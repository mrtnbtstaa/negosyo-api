import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from common.models.timestamp_model import TimestampModel
from django.contrib.auth import get_user_model

User = get_user_model()


class RoleChoice(models.TextChoices):
    OWNER = "owner", "Business Owner"
    CASHIER = "cashier", "Cashier"
    MANAGER = "manager", "Manager"


class Merchant(TimestampModel):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Linked to the merchant owner user
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="owned_stores",
        limit_choices_to={'account_type': 'owner'},
    )
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    category = models.CharField(max_length=100)
    
    business_email = models.EmailField(blank=True, null=True, unique=True)
    business_phone = PhoneNumberField(blank=True, null=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    
    # Branch & Location Info
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)  # Branch direct line
    
    # Operational Times (Fixes your time-check logic!)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    
    # Metrics & Media
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    review_count = models.PositiveIntegerField(default=0)
    image_public_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Setup status tracking
    setup_completed = models.BooleanField(default=False)
    setup_completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Merchant.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.branch_name or 'Main'})"


class MerchantStaff(TimestampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    merchant = models.ForeignKey(
        Merchant, 
        on_delete=models.CASCADE, 
        related_name="staff_members"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="merchant_employments",
        limit_choices_to={'account_type': 'staff'}
    )
    
    role = models.CharField(
        max_length=20,
        choices=RoleChoice.choices,
        default=RoleChoice.CASHIER
    )
    
    can_manage_orders = models.BooleanField(default=True)
    can_manage_catalog = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "user"],
                name="unique_merchant_staff",
            )
        ]

    def __str__(self):
        return f"{self.user.email} -> {self.merchant.name} ({self.role})"


class MerchantInvitation(TimestampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    merchant = models.ForeignKey(
        Merchant,
        on_delete=models.CASCADE,
        related_name="invitations",
    )

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=RoleChoice.choices,
    )

    accepted_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f"Invite: {self.email} for {self.merchant.name}"