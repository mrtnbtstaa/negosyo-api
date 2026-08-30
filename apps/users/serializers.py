from rest_framework import serializers
from common.serializers.fields import RequiredEmailField
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            "id",
            "email",  
        )

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