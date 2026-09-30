from rest_framework import serializers
from common.serializers.fields import RequiredCharField, RequiredEmailField, RequiredPhoneNumber, RequiredFileField, RequiredTimeField
from common.storage.storage_service import StorageService
from .models import Merchant
from .services import MerchantImageService
from datetime import datetime
from common.validators.password import validate_strong_password

class RegisterMerchantAccountSerializer(serializers.Serializer):
    
    full_name = RequiredCharField(
        write_only=True,
        label="Full name"
    )
    email = RequiredEmailField(
        write_only=True,
        label="Email"
    )
    password = RequiredCharField(
        write_only=True,
        label="Password",
        validators=[validate_strong_password]
    )

class CreateMerchantSerializer(serializers.Serializer):
    
    business_name = RequiredCharField(
            write_only=True,
            label="Business name"
        )
    business_category = RequiredCharField(
        write_only=True,
        label="Business category"
    )
    
    business_email = RequiredEmailField(
        write_only=True,
        label="Business email"
    )
    
    business_phone = RequiredPhoneNumber(
        write_only=True,
        label="Business phone"
    )
    
    description = RequiredCharField(
        write_only=True,
        label="Description"
    )
    
    branch_name = RequiredCharField(
        write_only=True,
        label="Branch name"
    )
    
    address = RequiredCharField(
        write_only=True,
        label="Address"
    )
    
    phone_number = RequiredPhoneNumber(
        write_only=True,
        label="Phone number"
    )
    
    opening_time = RequiredTimeField(
        write_only=True,
        label="Opening time",
        valid_format="HH:MM p",
        input_formats=["%H:%M %p"]
    )
    
    closing_time = RequiredTimeField(
        write_only=True,
        label="Closing time",
        valid_format="HH:MM p",
        input_formats=["%H:%M %p"]
    )
    
    image = RequiredFileField(
        write_only=True,
        label="Image"
    )
    
    def create(self, validated_data):
            
        user = self.context["request"].user
        
        public_id = MerchantImageService.upload_merchant_image(user, validated_data["image"])
        
        merchant = Merchant.objects.create(
            owner=user,
            name=validated_data.get("business_name"),
            category=validated_data.get("business_category"),
            business_email=validated_data.get("business_email"),
            business_phone=validated_data.get("business_phone"),
            description=validated_data.get("description"),
            branch_name=validated_data.get("branch_name"),
            address=validated_data.get("address"),
            phone_number=validated_data.get("phone_number"),
            opening_time=validated_data.get("opening_time"),
            closing_time=validated_data.get("closing_time"),
            image_public_id=public_id
        )
        
        user.onboarding_completed = True
        
        user.save(update_fields=["onboarding_completed"])
        
        return merchant

class ListMerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Merchant
        exclude = ("owner", "created_at", "updated_at")
        
    def to_representation(self, instance):
        
        data_representation = super().to_representation(instance)
        
        public_id = data_representation.pop("image_public_id")
        
        data_representation["image_url"] = StorageService.get_url(public_id=public_id)
        
        opening_time = getattr(instance, "opening_time", None)
        closing_time = getattr(instance, "closing_time", None)
        
        
        if opening_time and closing_time:
            
            current_time = datetime.now().time()
            
            if opening_time <= closing_time:
                # Standard hours (e.g., 09:00 to 17:00)
                is_open = opening_time <= current_time < closing_time
            else:
                # Overnight hours (e.g., 18:00 to 02:00)
                is_open = current_time >= opening_time or current_time < closing_time
            
            data_representation["is_open"] = is_open
        
        return data_representation

    
class DetailMerchantSerializer(serializers.ModelSerializer):
    
    opening_time = serializers.TimeField(format="%H:%M %p", read_only=True)
    closing_time = serializers.TimeField(format="%H:%M %p", read_only=True)
      
    class Meta:
        model = Merchant
        exclude = ("owner", "created_at", "updated_at")
    
    def to_representation(self, instance):
        
        data_representation = super().to_representation(instance)
        
        public_id = data_representation.pop("image_public_id")
        
        data_representation["image_url"] = StorageService.get_url(public_id=public_id)
        
        opening_time = getattr(instance, "opening_time", None)
        closing_time = getattr(instance, "closing_time", None)
        
        
        if opening_time and closing_time:
            
            current_time = datetime.now().time()
            
            if opening_time <= closing_time:
                # Standard hours (e.g., 09:00 to 17:00)
                is_open = opening_time <= current_time < closing_time
            else:
                # Overnight hours (e.g., 18:00 to 02:00)
                is_open = current_time >= opening_time or current_time < closing_time
            
            data_representation["is_open"] = is_open
            
        return data_representation
    
class UpdateBusinessInformationOnbordingSerializer(serializers.Serializer):
    
    onboarding_completed = serializers.BooleanField(write_only=True)
    setup_completed = serializers.BooleanField(write_only=True)
    
    
    