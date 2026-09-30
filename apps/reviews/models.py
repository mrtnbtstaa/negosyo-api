from django.db import models
from common.models.timestamp_model import TimestampModel
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Review(TimestampModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(to="merchants.Merchant", on_delete=models.CASCADE, related_name="merchants")
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="user_reviews")
    rating = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    comment = models.TextField(blank=True, null=True, max_length=500)
    
    
    # Database level constraints
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(rating__gte=1) & Q(rating__lte=5),
                name="rating_between_1_and_5"
            )
        ]
    
    def __str__(self):
        return       
