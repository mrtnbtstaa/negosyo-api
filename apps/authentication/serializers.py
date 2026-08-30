from rest_framework import serializers
from django.contrib.auth import get_user_model
from common.validators.password import validate_strong_password
from common.serializers.fields import RequiredCharField, RequiredEmailField
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from common.validators.files import ImageFileValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, 
    TokenRefreshSerializer,
    TokenVerifySerializer,
    TokenBlacklistSerializer
)

User = get_user_model()

# ------------------------------------------
# Token refresh serializer
# ------------------------------------------
class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    refresh = RequiredCharField(label="Refresh token")

# ------------------------------------------
# Verify token serializer
# ------------------------------------------
class CustomTokenVerifySerializer(TokenVerifySerializer):

    token = RequiredCharField(
        write_only=True,
        label="Token"
    )

# ------------------------------------------
# Blacklist token serializer
# ------------------------------------------
class LogoutBlacklistSerializer(TokenBlacklistSerializer):

    refresh = RequiredCharField(
        write_only=True,
        label="Refresh token"
    )

# ------------------------------------------
# Register serializer
# ------------------------------------------
class RegisterSerializer(serializers.Serializer):

    email = RequiredEmailField(
        write_only=True,
        label="Email",
        max_length=254
    )

    password = RequiredCharField(
        write_only=True,
        min_length=8,
        max_length=255,
        validators=[
            validate_strong_password,
            validate_password
        ],
        label="Password"
    )

    confirm_password = RequiredCharField(
        write_only=True,
        min_length=8,
        max_length=255,
        label="Confirm password",
        validators=[
            validate_password
        ]
    )

    profile_image = serializers.ImageField(
            required=False,
            allow_null=True,
            validators=[
                ImageFileValidator(),
            ],
        )

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": ["Passwords do not match."]
                }
            )

        return attrs

# ------------------------------------------
# Login serializer
# ------------------------------------------
class LoginSerializer(serializers.Serializer):

    email = RequiredCharField(
        write_only=True,
        label="Email"
    )

    password = RequiredCharField(
        write_only=True,
        label="Password"
    )
    
# ------------------------------------------
# Change password serializer
# ------------------------------------------
class ChangePasswordSerializer(serializers.Serializer):

    current_password = RequiredCharField(
        write_only=True,
        label="Current password",
    )

    new_password = RequiredCharField(
        write_only=True,
        min_length=8,
        max_length = 255,
        validators=[
            validate_strong_password,
            validate_password
        ],
        label="New password",
    )

    confirm_password = RequiredCharField(
        write_only=True,
        min_length=8,
        max_length = 255,
        label="Confirm password",
        validators=[validate_password]
    )

    def validate(self, attrs):

        request = self.context.get("request", None)

        # Checking if the password input matches to the hashed password
        if not check_password(attrs["current_password"], request.user.password):
            raise serializers.ValidationError(
                {
                    "current_password": ["Current password is incorrect."]
                }
            )

        if attrs["new_password"] == attrs["current_password"]:
            raise serializers.ValidationError(
                {
                    "new_password": ["New password must be different from your current password."]
                }
            )

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": ["Passwords do not match."]
                }
            )

        return attrs

# ------------------------------------------
# Forgot password serializer
# ------------------------------------------
class ForgotPasswordSerializer(serializers.ModelSerializer):

    email = RequiredEmailField(
        write_only=True,
        label="Email"
    )

    class Meta:
        model = User
        fields = ("email",)

# ------------------------------------------
# Reset password serializer
# ------------------------------------------
class ResetPasswordSerializer(serializers.Serializer):

    uid = RequiredCharField(
        write_only=True,
        label="Uid"
    )
    token = RequiredCharField(
        write_only=True,
        label="Token"
    )
    new_password = RequiredCharField(
        write_only=True,
        min_length=8,
        max_length=255,
        label="New password",
        validators=[
            validate_strong_password,
            validate_password
        ]
    )
    confirm_password = RequiredCharField(
        write_only=True,
        min_length=8,
        max_length=255,
        label="Confirm password",
        validators=[validate_password]
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": ["Passwords do not match."]
                }
            )

        return attrs

# ------------------------------------------
# Verify email serializer
# ------------------------------------------
class VerifyEmailSerializer(serializers.Serializer):

    uid = RequiredCharField(label="Uid")
    token = RequiredCharField(label="Token")


# ------------------------------------------
# Resend verification serializer
# ------------------------------------------
class ResendVerificationSerializer(serializers.ModelSerializer):

    email = RequiredEmailField(write_only=True, label="Email")

    class Meta:
        model = User
        fields = ("email",)



# ------------------------------------------
# Me/Profile serializer
# ------------------------------------------
class MeSerializer(serializers.Serializer):

    email = RequiredEmailField(
        write_only=True,
        label="Email"
    )

    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
        validators=[
            ImageFileValidator(),
        ],
    )

