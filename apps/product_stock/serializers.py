from rest_framework import serializers
from common.serializers.fields import RequiredCharField, RequiredDecimalField, RequiredFileField, RequiredIntegerField
from .models import ProductStock
from apps.suppliers.selectors import SupplierSelector
from common.exceptions.api import NotFoundException
from common.storage.storage_service import StorageService
from .utils import calculate_stock_status

class CreateProductStockSerializer(serializers.Serializer):
    
    category = RequiredCharField(
        write_only=True,
        label="Category"
    )
    
    product_name = RequiredCharField(
        write_only=True,
        label="Product name"
    )
    
    description = RequiredCharField(
        write_only=True,
        label="Description"
    )
    
    product_image = RequiredFileField(
        write_only=True,
        label="Product image"
    )
    
    retail_selling_price = RequiredDecimalField(
        write_only=True,
        label="Retail selling price"
    )
    
    cogs = RequiredDecimalField(
        write_only=True,
        label="Retail selling price"
    )
    
    stock_quantity = RequiredIntegerField(
        write_only=True,
        label="Stock quantity"
    )
    
    low_stock_threshold = RequiredIntegerField(
        write_only=True,
        label="Low stock threshold"
    )
    
    suppliers = RequiredCharField(
        write_only=True,
        label="Suppliers"
    )
        
    def validate(self, attrs):
        
        supplier = SupplierSelector.get_or_none(company_name=attrs["suppliers"])
        
        if supplier is None:
            raise NotFoundException(errors={
                "suppliers": ["No supplier found."]
            })
        
        valid_category = ["beverages", "dairy", "bakery", "packaging", "general"]
        
        if attrs["category"] not in valid_category:
            raise serializers.ValidationError({
                "category": ["Category invalid value"]
            })
            
        attrs["suppliers"] = supplier
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("product_image", None)
        return ProductStock.objects.create(**validated_data)
        
        
class ProductStockSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductStock
        exclude = ("suppliers", "created_at", "updated_at")
    
    def to_representation(self, instance):
        
        data_representation = super().to_representation(instance)
        
        stock_threshold = data_representation.pop("low_stock_threshold")
        
        data_representation["stock_status"] = calculate_stock_status(instance.stock_quantity, stock_threshold)
        
        public_id = data_representation.pop("product_image_public_id")
        
        if public_id:
            data_representation["product_image_url"] = StorageService.get_url(public_id=public_id) or None
        
        data_representation["merchant_id"] = data_representation.pop("merchant")
            
        return data_representation
    
    
class UpdateProductStockSerializer(serializers.ModelSerializer):
    
    category = RequiredCharField(
        write_only=True,
        label="Category"
    )
    
    product_name = RequiredCharField(
        write_only=True,
        label="Product name"
    )
    
    product_image = serializers.FileField(
        write_only=True,
        required=False,
        allow_null=True
    )
    
    retail_selling_price = RequiredDecimalField(
        write_only=True,
        label="Retail selling price"
    )
    
    cogs = RequiredDecimalField(
        write_only=True,
        label="Retail selling price"
    )
    
    class Meta:
        model = ProductStock
        fields = (
            "category", "product_name",
            "product_image", "retail_selling_price",
            "cogs"
        )
    
        
    def validate(self, attrs):
        
        valid_category = ["beverages", "dairy", "bakery", "packaging", "general"]
        
        if attrs["category"] not in valid_category:
            raise serializers.ValidationError({
                "category": ["Category invalid value"]
            })
            
            
        return attrs
    

class UpdateProductQuantitySerializer(serializers.ModelSerializer):
    
    stock_quantity = RequiredIntegerField(
        write_only=True,
        label="Quantity"
    )
    
    reason = serializers.CharField(
        write_only=True,
        allow_null=True,
        allow_blank=True,
        required=False
    )
    
    class Meta:
        model = ProductStock
        fields = ("stock_quantity", "reason")
    
    
class ProductStockSummarySerializer(serializers.Serializer):
    
    total_sku = serializers.IntegerField(read_only=True)
    skus_this_month = serializers.IntegerField(read_only=True)
    low_stock_count = serializers.IntegerField(read_only=True)
    total_stock_value = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=12)
    
