from django.contrib import admin
from .models import Merchant, MerchantInvitation, MerchantStaff

@admin.register(Merchant)
class Merchant(admin.ModelAdmin):
    pass

@admin.register(MerchantInvitation)
class MerchantInvitation(admin.ModelAdmin):
    pass

@admin.register(MerchantStaff)
class MerchantStaff(admin.ModelAdmin):
    pass