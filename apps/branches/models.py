from django.db import models
from common.models.timestamp_model import TimestampModel
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Branch(TimestampModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(to="merchants.Merchant", on_delete=models.CASCADE, related_name="branches")

    branch_name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    phone_number = PhoneNumberField()
    operating_hours = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f"Merchants: {self.address}"

class BranchMember(TimestampModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE, related_name="members")
    merchant_member = models.ForeignKey(to="merchants.MerchantStaff", on_delete=models.CASCADE, related_name="branch_members")


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "merchant_member"],
                name="unique_branch_member"
            )
        ]
     
    
    def __str__(self):
        return f"Branch name: {self.branch.branch_name}"