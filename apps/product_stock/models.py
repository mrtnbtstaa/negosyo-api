from django.db import models
from common.models.timestamp_model import TimestampModel
import uuid
from django.core.validators import MinValueValidator
from django.utils import timezone

class ProductStockStatusChoice(models.TextChoices):
    
    IN_STOCK = "in stock", "In Stock"
    LOW_STOCK = "low stock", "Low Stock"
    OUT_OF_STOCK = "out of stock", "Out of Stock"

class ProductCategoryChoice(models.TextChoices):
    
    BEVERAGES = "beverages", "Beverages"
    DAIRY = "dairy", "Dairy"
    BAKERY = "bakery", "Bakery"
    PACKAGING = "packaging", "Packaging"
    GENERAL = "general", "General"

class ProductStock(TimestampModel):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    merchant = models.ForeignKey(to="merchants.Merchant", on_delete=models.CASCADE, related_name="product_stocks")
    
    suppliers = models.ForeignKey(to="suppliers.Supplier", null=True, on_delete=models.SET_NULL, related_name="products")
    
    sku = models.CharField(max_length=30)
    
    category = models.CharField(choices=ProductCategoryChoice.choices)
    
    description = models.TextField(max_length=255, null=True, blank=True)
    
    product_name = models.CharField(max_length=50)
    
    product_image_public_id = models.CharField(max_length=255)
    
    retail_selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    cogs = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0)
        ]
    )
    
    stock_quantity = models.BigIntegerField(
        validators=[
            MinValueValidator(0)
        ]
    )
    
    low_stock_threshold = models.BigIntegerField(
        validators=[
            MinValueValidator(0)
        ]
    ) 
    
    stock_status = models.CharField(choices=ProductStockStatusChoice.choices, default=ProductStockStatusChoice.IN_STOCK.value)
    
    reason = models.TextField(
        max_length=255,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.sku
    
    def save(self, *args, **kwargs):
    
        if not self.sku:
            
            year = timezone.now().year
            
            last_sku = (
                ProductStock.objects
                .filter(
                    merchant=self.merchant,
                    sku__startswith=f"SKU-"
                )
                .order_by("-created_at")
                .first()
            ) 
            if last_sku:
                last_number = int(last_sku.sku.split("-")[-1])
                next_number = last_number + 1
            else:
                next_number = 1
                
            self.sku = f"SKU-{next_number:03d}"
            
        return super().save(*args, **kwargs)
        
