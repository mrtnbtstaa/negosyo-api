from django.db import models
from django.contrib.auth import get_user_model
from common.models.timestamp_model import TimestampModel
import uuid
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

class GenderChoice(models.TextChoices):
    male = ("MALE", "Male")
    female = ("FEMALE", "Female")

class Customer(TimestampModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="customer")

    address = models.TextField(null=True, blank=True, max_length=100)
    gender = models.CharField(choices=GenderChoice.choices, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return f"Customer: {self.user.email}"
    