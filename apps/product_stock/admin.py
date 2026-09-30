from django.contrib import admin
from .models import ProductStock

@admin.register(ProductStock)
class ProductStock(admin.ModelAdmin):
    pass