from django.db import models
from common.models.timestamp_model import TimestampModel
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Action(models.TextChoices):
    CREATED = "CREATED", "Created"
    UPDATED = "UPDATED", "Updated"
    DELETED = "DELETED", "Deleted"
    LOGIN = "LOGIN", "Login"
    LOGIN_FAILED = "LOGIN FAILED", "Login Failed"
    LOGOUT = "LOGOUT", "Logout"
    REGISTER = "REGISTER", "Register"
    PASSWORD_CHANGE = "PASSWORD_CHANGE", "Password Change"
    PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION", "Email Verification"
    RESEND_EMAIL_VERIFICATION = "RESEND_EMAIL_VERIFICATION", "Resend Email Verification"
    FORGOT_PASSWORD = "FORGOT_PASSWORD", "Forgot Password"

class AuditLog(TimestampModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )

    action = models.CharField(
        max_length=50,
        choices=Action.choices,
    )

    module_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True,
    )

    original = models.JSONField(
        blank=True,
        null=True
    )

    changes = models.JSONField(
        blank=True,
        null=True,
    )

    user_agent = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


    class Meta:
        db_table = "audit_logs"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("user",)),
            models.Index(fields=("module_name",))
        ]


    def __str__(self):
        return f"{self.module_name} - {self.action}" if self.user is not None else "Anonymous User"