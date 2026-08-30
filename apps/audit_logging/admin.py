from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AdminAuditLog(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")