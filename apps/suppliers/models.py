import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.payment_term_choices import PaymentTermChoices
from common.models.timestamp_model import TimestampModel

class SupplierCategoryChoices(models.TextChoices):
    FOOD = "food", "Food"
    BEVERAGE = "beverages", "Beverages"
    ELECTRONICS = "electronics", "Electronics"
    OFFICE = "office", "Office"
    SERVICES = "services", "Services"

class Supplier(TimestampModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    merchant = models.ForeignKey(
        "merchants.Merchant",
        on_delete=models.CASCADE,
        related_name="suppliers",
    )

    company_name = models.CharField(
        max_length=100,
    )

    category = models.CharField(
        choices=SupplierCategoryChoices.choices
    )

    payment_terms = models.CharField(
        max_length=20,
        choices=PaymentTermChoices.choices,
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone_number = PhoneNumberField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["merchant", "company_name"],
                name="unique_supplier_company_per_merchant",
            ),
            models.UniqueConstraint(
                fields=["merchant", "email"],
                condition=~models.Q(email=""),
                name="unique_supplier_email_per_merchant",
            ),
        ]

    def __str__(self):
        return self.company_name