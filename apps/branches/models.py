from django.db import models
from common.models.timestamp_model import TimestampModel
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class Branch(TimestampModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    business = models.ForeignKey(to="business.Business", on_delete=models.CASCADE, related_name="branches")

    branch_name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    phone_number = PhoneNumberField()
    operating_hours = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)


class BranchMember(TimestampModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(to=Branch, on_delete=models.CASCADE, related_name="members")
    business_member = models.ForeignKey(to="business.BusinessMember", on_delete=models.CASCADE, related_name="branch_members")


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["branch", "business_member"],
                name="unique_branch_member"
            )
        ]
     