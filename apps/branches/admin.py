from django.contrib import admin
from .models import Branch, BranchMember


@admin.register(Branch)
class Branch(admin.ModelAdmin):
    pass

@admin.register(BranchMember)
class BranchMember(admin.ModelAdmin):
    pass