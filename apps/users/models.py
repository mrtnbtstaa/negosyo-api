import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models.timestamp_model import TimestampModel
from .manager import CustomUserManager
# Create your models here.

class User(AbstractUser, TimestampModel):

    username = None 

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


    