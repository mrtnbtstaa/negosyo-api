from common.views.viewsets import BaseModelViewSet
from common.views.api import ProtectedBaseAPiView
from common.permission.permission import IsOwnerPermission
from .selectors import ProductStockSelector
from .services import ProductImageService
from rest_framework.decorators import action
from common.responses.success import OkResponse
from common.exceptions.api import NotFoundException
from rest_framework.parsers import MultiPartParser, FormParser
from common.constants.messages import Messages
from .models import ProductStock
from django.db.models import Count, Q, F, Sum
from django.utils import timezone
from .services import ProductStockService
from apps.merchants.models import Merchant
from .serializers import (
    CreateProductStockSerializer,
    ProductStockSerializer,
    UpdateProductStockSerializer,
    UpdateProductQuantitySerializer,
    ProductStockSummarySerializer
)

class ProductStockViewSet(BaseModelViewSet, ProtectedBaseAPiView):
    
    parser_classes = [MultiPartParser, FormParser]
    
    selector = ProductStockSelector
    
    serializer_action_classes = {
        "create": CreateProductStockSerializer,
        "list": ProductStockSerializer,
        "retrieve": ProductStockSerializer,
        "partial_update": UpdateProductStockSerializer,
        "update": UpdateProductStockSerializer,
        "quantity": UpdateProductQuantitySerializer
    }
    
    @action(detail=True, methods=["PATCH"], permission_classes=[IsOwnerPermission])
    def quantity(self, request, pk=None):
        
        product_stock = self.get_object() # Fetches the product stock using the standard ID
        
        serializer = UpdateProductQuantitySerializer(
            product_stock,
            data=request.data,
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        
        validated_data = serializer.validated_data
        
        ProductStockService.adjust_quantity(
            product_stock,
            validated_data["stock_quantity"],
        )
        
        serializer.save()
        
        return OkResponse(
            message=Messages.UPDATED,
        )
        
    @action(detail=False, methods=["GET"], permission_classes=[IsOwnerPermission])
    def summary(self, request, pk=None):
        
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        owned_store = request.user.owned_stores.first()
        
        if owned_store is None:
            raise NotFoundException(message=Messages.NOT_FOUND)
        
        product = (
            ProductStock
            .objects
            .filter(merchant=owned_store)
            .aggregate(
                total_sku=Count("id"),
                skus_this_month=Count("id", filter=Q(created_at__gte=start_of_month)),
                low_stock_count=Count("id", filter=Q(stock_status="low stock")),
                total_stock_value=Sum(F("stock_quantity") * F("retail_selling_price"))   
            )
        )
       
        serializer = ProductStockSummarySerializer(product)
        
        return OkResponse(
            message=Messages.OK,
            data=serializer.data
        )
        
    def perform_update(self, serializer):
        
        validated_data = serializer.validated_data

        image = validated_data.get("product_image", None)
        
        if image:
            ProductImageService.update_product_image(
                self.request.user,
                image
            )
        
        return super().perform_update(serializer)
    
    def perform_create(self, serializer):
        
        validated_data = serializer.validated_data
        
        image = validated_data["product_image"]
        
        owned_store = getattr(
            self.request.user,
            "owned_stores",
            None
        ).first()
        
        upload_public_id = ProductImageService.upload_product_image(
            self.request.user,
            image
        )
        
        serializer.save(
            merchant=owned_store,
            product_image_public_id=upload_public_id
        )
    