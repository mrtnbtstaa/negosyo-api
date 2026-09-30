from rest_framework import serializers
from .models import User, UserInformation
from common.serializers.fields import (
    RequiredEmailField, 
    RequiredCharField,
    RequiredDateField,
    RequiredPhoneNumber,
)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "email",  
            "account_type",
            "onboarding_completed"
        )
        
    def to_representation(self, instance):
        
        data_representation = super().to_representation(instance)
        
        account_type = data_representation.get("account_type")
        
        if account_type != "owner":
            data_representation.pop("onboarding_completed")
        
        return data_representation
        
class CurrentUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("account_type", "onboarding_completed")

class UpdateUserSerializer(serializers.ModelSerializer):

    email = RequiredEmailField(
        write_only=True,
        label="Email"
    )

# ------------------------------------------
# Resend verification serializer
# ------------------------------------------
class ResendVerificationSerializer(serializers.ModelSerializer):

    email = RequiredEmailField(write_only=True, label="Email")

    class Meta:
        model = User
        fields = ("email")
        
        
class UpdateUserMeSerializer(serializers.Serializer):
    
    full_name = RequiredCharField(
        write_only=True,
        label="Full name"
    )
    
    email = RequiredEmailField(
        write_only=True,
        label="Email"
    )
    
    phone_number = RequiredPhoneNumber(
        write_only=True,
        label="Phone number"
    )
    
    gender = RequiredCharField(
        write_only=True,
        label="Gender"
    )
    
    date_of_birth = RequiredDateField(
        write_only=True,
        label="Date of birth",
        input_formats=["%Y-%m-%d"]
    )
    
    def validate(self, attrs):
        
        if attrs["gender"] not in ["female", "male"]:
            raise serializers.ValidationError({
                "errors": ["Invalid gender value."]
            })
        
        return attrs
    
    def update(self, instance, validated_data):

        instance.email = validated_data.get(
            "email",
            instance.email
        )

        instance.full_name = validated_data.get(
            "full_name",
            instance.full_name
        )

        instance.save(
            update_fields=[
                "email",
                "full_name",
            ]
        )
    
    
        UserInformation.objects.update_or_create(
            user=instance,
            defaults={
                "phone_number":validated_data.get("phone_number", None),
                "gender":validated_data.get("gender", None),
                "date_of_birth":validated_data.get("date_of_birth", None)
            }
        )


        return instance
    
    
class UserMeSerializer(serializers.ModelSerializer):
    
    phone_number = serializers.CharField(source="user_information.phone_number")
    gender = serializers.CharField(source="user_information.gender")
    date_of_birth = serializers.CharField(source="user_information.date_of_birth")
    
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "gender",
            "date_of_birth"
        )
        
        

    
