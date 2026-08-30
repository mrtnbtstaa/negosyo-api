from rest_framework import serializers
from common.validators.files import ImageFileValidator

class ProfileSerializer(serializers.Serializer):

    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
        validators=[
            ImageFileValidator(),
        ],
    )

