from common.selectors.base import BaseSelector
from .models import Cart, CartItem

class CartSelector(BaseSelector):

    model = Cart    
    
    
class CartItemSelector(BaseSelector):
    
    model = CartItem