from django.contrib import admin
from .models import Supplier

@admin.register(Supplier)
class Supplier(admin.ModelAdmin):
    pass