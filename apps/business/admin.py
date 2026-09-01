from django.contrib import admin
from .models import Business, BusinessMember

@admin.register(Business)
class Business(admin.ModelAdmin):
    pass

@admin.register(BusinessMember)
class BusinessMember(admin.ModelAdmin):
    pass