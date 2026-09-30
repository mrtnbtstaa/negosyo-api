from django.contrib import admin
from .models import PurchaseOrder

@admin.register(PurchaseOrder)
class PurchaseOrder(admin.ModelAdmin):
    readonly_fields = ("po_number", )