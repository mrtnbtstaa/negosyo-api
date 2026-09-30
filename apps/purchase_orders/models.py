import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from common.models.timestamp_model import TimestampModel
from common.models.payment_term_choices import PaymentTermChoices

class PurchaseOrderChoices(models.TextChoices):
    
    IN_TRANSIT = "in transit", "In Transit"
    PENDING = "pending", "Pending"
    DELIVERED = "delivered", "Delivered"

class PurchaseOrder(TimestampModel):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    merchant = models.ForeignKey(
        "merchants.Merchant",
        on_delete=models.CASCADE,
        related_name="purchase_orders",
    )
    
    po_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        null=True
    )

    supplier_name = models.CharField(
        max_length=100,
    )

    items = models.JSONField(
        default=list,
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    payment_terms = models.CharField(
        choices=PaymentTermChoices.choices
    )
    
    status = models.CharField(
        choices=PurchaseOrderChoices.choices,
        null=True
    )

    
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_amount__gte=0),
                name="purchase_order_total_amount_gte_zero"
            ),
            models.UniqueConstraint(
                fields=["merchant", "po_number"],
                name="unique_merchant_po_number"
            )
        ]
    
    def __str__(self):
        return self.supplier_name
    
    def save(self, *args, **kwargs):
        
        if not self.po_number:
            
            year = timezone.now().year
            
            last_po = (
                PurchaseOrder.objects
                .filter(
                    business=self.business,
                    po_number__startswith=f"PO-{year}-"
                )
                .order_by("-created_at")
                .first()
            ) 
            if last_po:
                last_number = int(last_po.po_number.split("-")[-1])
                next_number = last_number + 1
            else:
                next_number = 1
                
            self.po_number = f"PO-{year}-{next_number:03d}"
            
        return super().save(*args, **kwargs)
    