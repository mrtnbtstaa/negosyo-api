from rest_framework import serializers
from .models import PurchaseOrder
from common.serializers.fields import RequiredCharField, RequiredDecimalField, RequiredListField

class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
    
    supplier_name = RequiredCharField(
        write_only=True,
        label="Supplier name"
    )
    items = RequiredListField(
        write_only=True,
        label="Items",
        min_length=1
    )
    total_amount = RequiredDecimalField(
        write_only=True,
        label="Total amount"
    )   
    payment_terms = RequiredCharField(
        write_only=True,
        label="Payment terms"
    )
    
    def validate_total_amount(self, value):
        
        if value < 0:
            raise serializers.ValidationError({
                "total_amount": ["Total ammount cannot be negative."]
            })
            
        return value
            
    class Meta:
        model = PurchaseOrder
        exclude = ("id", "business", "created_at", "updated_at")        
        
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseOrder
        exclude = ("business", "updated_at")
        
class DetailPurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseOrder
        exclude = ("business", "created_at", "updated_at")
        
        
from rest_framework import serializers

class PurchaseOrderSummarySerializer(serializers.Serializer):
    
    total_order = serializers.IntegerField()
    total_transit = serializers.IntegerField()
    total_delivered = serializers.IntegerField()
    total_procurement = serializers.DecimalField(max_digits=12, decimal_places=2)
