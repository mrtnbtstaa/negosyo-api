from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from common.models.timestamp_model import TimestampModel
import uuid

User = get_user_model()


class RoleChoice(models.TextChoices):
    OWNER = "owner", "Business Owner"
    CASHIER = "cashier", "Cashier"
    MANAGER = "manager", "Manager"


class Business(TimestampModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="owned_business",
        null=True
    )

    business_name = models.CharField(
        max_length=30,
    )

    business_category = models.CharField(
        max_length=30,
    )

    business_email = models.EmailField(
        unique=True,
        max_length=30,
    )

    business_phone = PhoneNumberField()


class BusinessMember(TimestampModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="members",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=RoleChoice.choices,
    )

    is_active = models.BooleanField(default=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business", "user"],
                name="unique_business_member",
            )
        ]