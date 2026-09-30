from common.selectors.base import BaseSelector
from common.constants.messages import Messages
from .models import Supplier
from django.contrib.auth.models import AbstractUser
from common.exceptions.api import PermissionDeniedException

class SupplierSelector(BaseSelector):
    
    model = Supplier
    
    searchable_fields = ("company_name", "email")
    
    filterable_fields = {
        "category": ("exact", ),
        "payment_terms": ("exact", )
    }
    
    @classmethod
    def check_owner_permission(cls, user):
        
        if user.account_type != "owner":
            raise PermissionDeniedException(message=Messages.FORBIDDEN)
    
    @classmethod
    def get_supplier_by_owner(cls, user: AbstractUser):
        
        cls.check_owner_permission(user)
        
        return cls.get_queryset()