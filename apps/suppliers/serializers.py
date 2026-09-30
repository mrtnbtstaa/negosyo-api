from rest_framework import serializers
from .models import Supplier, SupplierCategoryChoices
from common.serializers.fields import RequiredCharField, RequiredEmailField, RequiredPhoneNumber
from common.validators.email import validate_safe_email
from common.exceptions.api import ConflictException
from .selectors import SupplierSelector
from common.constants.messages import Messages
from common.constants.choices import payment_term_choices

class CreateSupplierSerializer(serializers.ModelSerializer):
    
    company_name = RequiredCharField(
        write_only=True,
        label="Company name"
    )
    
    category = RequiredCharField(
        write_only=True,
        label="Category"
    )
    
    payment_terms = RequiredCharField(
        write_only=True,
        label="Payment terms"
    )
    
    contact_person = RequiredCharField(
        write_only=True,
        label="Contact person"
    )
    
    email = RequiredEmailField(
        write_only=True,
        label="Email",
        validators=[
            validate_safe_email
        ]
    )
    
    phone_number = RequiredPhoneNumber(
        write_only=True,
        label="Phone number"
    )
    
    class Meta:
        model = Supplier
        exclude = ("id", "merchant")
        
    def validate(self, attrs):

        category_choices = ["food", "beverages", "electronics", "office", "services"]
            
        if SupplierSelector.exists(email=attrs["email"]):
            raise ConflictException(errors={
                "email": ["Email already exists."]
            })
            
        if attrs["category"] not in category_choices:
            raise serializers.ValidationError({
                "category": ["Invalid category value."]
            })
            
        if attrs["payment_terms"] not in payment_term_choices():
            raise serializers.ValidationError({
                "payment_terms": ["Invalid payment term value."]
            })    
        
        return attrs
        
        
class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Supplier
        exclude = (
            "business",
            "created_at",
            "updated_at"
        )