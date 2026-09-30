from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class Cart(admin.ModelAdmin):
    pass

@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    pass