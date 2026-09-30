import uuid
from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models.timestamp_model import TimestampModel
from .manager import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField

CATEGORY_CHOICES = [
    ("bakeries", "Bakeries"),
    ("cafes", "Cafes"),
    ("grocery", "Grocery"),
    ("meat", "Meat"),
]

class AccountTypeChoice(models.TextChoices):
    
    OWNER = ("owner", "Owner")
    STAFF = ("staff", "Staff")
    CUSTOMER = ("customer", "Customer")

class User(AbstractUser, TimestampModel):

    username = None 

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    full_name = models.CharField(null=True)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    onboarding_completed = models.BooleanField(
        default=False,
    )
    
    account_type = models.CharField(choices=AccountTypeChoice.choices, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


class UserInformation(TimestampModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="user_information")
    phone_number = PhoneNumberField(null=True, max_length=13)
    gender = models.CharField(null=True)
    date_of_birth = models.DateField(null=True)
    
    
class UserAddress(TimestampModel):
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_address")
    
    address_tag = models.CharField(null=True, max_length=20)
    address = models.TextField(null=True, max_length=100)
    recipient_name = models.CharField(null=True, max_length=30)
    contact_number = PhoneNumberField(null=True, max_length=13)
    active_address = models.BooleanField(default=False)


