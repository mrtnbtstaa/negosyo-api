from django.contrib import admin
from .models import User, UserInformation, UserAddress
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(UserInformation)
class UserInformation(admin.ModelAdmin):
    pass

@admin.register(UserAddress)
class UserAddress(admin.ModelAdmin):
    pass

