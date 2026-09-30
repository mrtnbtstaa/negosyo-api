from uuid import uuid4

from common.storage.storage_service import StorageService
from common.validators.files import ImageFileValidator
from common.constants.messages import Messages
from common.exceptions import NotFoundException
from django.db import transaction
from .utils import calculate_stock_status
from .models import ProductStock
from .selectors import ProductStockSelector
from .enum import ModeEnum
class ProductImageService:
    
    """
    Cloudinary storage service.

    Responsible only for uploading an image product.
    """
    def __new__(cls):
        raise TypeError("ProductImageService cannot be instantiated.")

    @staticmethod
    def update_product_image(
        user,
        image,
    ):
        
        ImageFileValidator()(image)

        # Safely access the owned business
        owned_stores = getattr(user, "owned_stores", None)
        
        product = ProductStockSelector.get_or_none(merchant=owned_stores)
        
        if product is None:
            raise NotFoundException(
                message=Messages.NOT_FOUND
            )

        result = StorageService.upload(
            file=image,
            public_id=product.product_image_public_id,
        )

        # Delete previous product image after successful upload.
        if product.product_image_public_id:
            StorageService.delete(
                public_id=product.product_image_public_id,
            )

        product.product_image_public_id = result["public_id"]

        product.save(
            update_fields=[
                "product_image_public_id"
            ]
        )

        return product

    @staticmethod
    def upload_product_image(
        user,
        image
    ) -> str:

        # ImageFileValidator()(image)
        
        # The generated public_id with a uuid to make the public id unique
        public_id = f"{user.id}/images/{uuid4()}"

        result = StorageService.upload(
            file=image,
            public_id=public_id,
            folder="products"
        )

        return result["public_id"]
    
class ProductStockService:

    @staticmethod
    @transaction.atomic
    def update_quantity(
        product_stock: ProductStock,
        quantity: int,
    ) -> ProductStock:

        if quantity < 0:
            raise ValueError(
                "Stock quantity cannot be negative."
            )

        product_stock.stock_quantity = quantity

        product_stock.stock_status = calculate_stock_status(
            stock_quantity=quantity,
            low_stock_threshold=product_stock.low_stock_threshold,
        )

        product_stock.save(
            update_fields=[
                "stock_quantity",
                "stock_status",
                "updated_at",
            ]
        )

        return product_stock

    @staticmethod
    @transaction.atomic
    def adjust_quantity(
        product_stock: ProductStock,
        quantity_delta: int,
    ) -> ProductStock:

        product_stock.stock_status = calculate_stock_status(
            stock_quantity=quantity_delta,
            low_stock_threshold=product_stock.low_stock_threshold,
        )
        
        product_stock.save(
            update_fields=[
                "stock_quantity",
                "stock_status",
                "updated_at",
            ]
        )

        return product_stock

    @staticmethod
    @transaction.atomic
    def update_threshold(
        product_stock: ProductStock,
        threshold: int,
    ) -> ProductStock:

        if threshold < 0:
            raise ValueError(
                "Low stock threshold cannot be negative."
            )

        product_stock.low_stock_threshold = threshold

        product_stock.stock_status = calculate_stock_status(
            stock_quantity=product_stock.stock_quantity,
            low_stock_threshold=threshold,
        )

        product_stock.save(
            update_fields=[
                "low_stock_threshold",
                "stock_status",
                "updated_at",
            ]
        )

        return product_stock