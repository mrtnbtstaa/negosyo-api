from django.db import models
from django.contrib.auth import get_user_model
import uuid
from common.models.timestamp_model import TimestampModel

User = get_user_model()

class Profile(TimestampModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile"
    )

    profile_public_id = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )

    profile_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    profile_size = models.PositiveBigIntegerField(
        blank=True,
        null=True,
    )

    profile_content_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    @staticmethod
    def create_profile(
        user,
        profile_public_id,
        profile_size,
        profile_content_type,
        profile_name
    ):
        return Profile.objects.create(
            user=user,
            profile_public_id=profile_public_id,
            profile_size=profile_size,
            profile_content_type=profile_content_type,
            profile_name=profile_name
        )

    def __str__(self):
        return f"User Profile: {self.user.email}"