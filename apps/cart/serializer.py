from rest_framework import serializers
from .models import Cart, CartItem
from common.serializers.fields import RequiredCharField
from apps.product_stock.selectors import ProductStockSelector
from common.exceptions.api import NotFoundException
from common.constants.messages import Messages
from apps.product_stock.serializers import ProductStockSerializer
from apps.merchants.selectors import MerchantSelector
from apps.product_stock.models import ProductStock
from django.db import transaction
from django.db.models import F
from decimal import Decimal

class CreateCartSerializer(serializers.Serializer):
    
    merchant = RequiredCharField(
        write_only=True,
        label="Merchant"
    )
    product = RequiredCharField(
        write_only=True,
        label="Product"
    )
    quantity = serializers.IntegerField()
    
    @transaction.atomic
    def create(self, validated_data):
        
        # Current authenticated user
        user = self.context["request"].user
    
        # Get the user's active cart or create one if it doesn't exist
        cart, _ = Cart.objects.get_or_create(user=user)
        
        # Extract data from validated payload
        product = validated_data["product"] 
        merchant = validated_data["merchant"]
        additional_quantity = validated_data.get("quantity", 1) # Default to 1 if not specified
        
        # Validate product existence, return 404 if not found
        product_obj = ProductStockSelector.get_or_none(id=product)
        if product_obj is None:
            raise NotFoundException(message=Messages.NOT_FOUND)
            
        # Validate merchant existence, return 404 if not found
        merchant_obj = MerchantSelector.get_or_none(id=merchant)
        if merchant_obj is None:
            raise NotFoundException(message=Messages.NOT_FOUND)
        
        # Get or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product_obj,
            defaults={
                "merchant": merchant_obj,
                "quantity": additional_quantity
            }
        )
        
        # If the item already existed, increment its quantity atomically using F()
        if not created:
            CartItem.objects.filter(pk=cart_item.pk).update(quantity=F("quantity") + additional_quantity)
            # Refresh the instance from the db so it returns the updated quantity
            cart_item.refresh_from_db()
            
        return cart_item

class CartItemDetailSerializer(serializers.ModelSerializer):
    
    product = ProductStockSerializer(read_only=True)
    cart_item_id = serializers.CharField(source="id")
    class Meta:
        model = CartItem
        fields = ("cart_item_id", "product", "quantity")
        
        
    def to_representation(self, instance):
        
        representation = super().to_representation(instance)

        product_data = representation.pop("product", {})
        
        if "id" in product_data:
            product_data["product_id"] = product_data.pop("id")
        
        # Merge product fields into the root level
        representation.update(product_data)
        
        if "reason" in product_data:
            representation.pop("reason")
            
        if "stock_status" in product_data:
            representation.pop("stock_status")
            
        if "cogs" in product_data:
            representation.pop("cogs")
            
        quantity = representation.get("quantity", 1)
        
        representation["total_amount"] = quantity * Decimal(representation.get("retail_selling_price", 1))
            
        return representation
        
class ListCartSerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()
    cart_id = serializers.CharField(source="id")
    
    def get_products(self, obj):
        
        cart_items = obj.items.select_related("product", "merchant").all()
        
        return CartItemDetailSerializer(cart_items, many=True).data
    
    class Meta:
        model = CartItem
        fields = ("cart_id", "products", "quantity")
        
class DetailCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        read_only_fields = ("id", "user", "product")
