from django.db import models
from common.models.timestamp_model import TimestampModel
from django.contrib.auth import get_user_model
import uuid
from django.core.validators import MinValueValidator

User = get_user_model()

class Cart(TimestampModel):
    
    """Represents a user's active shopping cart session."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="carts")
    
    class Meta:
        # Composite Indexing
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.email}"
    
    
class CartItem(TimestampModel):
    
    """Individual items inside a user's cart."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, related_name="items")
    
    product = models.ForeignKey(
        to="product_stock.ProductStock",
        on_delete=models.CASCADE,
        related_name="product_carts"
    )
    merchant = models.ForeignKey(
        to="merchants.Merchant",
        on_delete=models.SET_NULL,
        related_name="cart_items",
        null=True
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    class Meta:
        # Prevents duplicate rows for the same product in the same cart
        constraints = [
            models.UniqueConstraint(fields=["cart", 'product'], name="unique_cart_product")
        ]
        
    def __str__(self):
        return f"{self.quantity}x {self.product.product_name} in Cart {self.cart.id}"
