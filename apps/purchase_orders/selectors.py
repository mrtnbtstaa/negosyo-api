from common.selectors.base import BaseSelector
from common.constants.messages import Messages
from common.exceptions.api import PermissionDeniedException
from .models import PurchaseOrder
from django.contrib.auth.models import AbstractUser

class PurchaseOrderSelector(BaseSelector):
    
    model = PurchaseOrder
    
    searchable_fields = ("po_number", )
    
    filterable_fields = {
        "status": ("exact", )
    }
    
    @classmethod
    def check_owner_permission(cls, user: AbstractUser):
        
        if user.account_type != "owner":
            raise PermissionDeniedException(message=Messages.FORBIDDEN)
        
    @classmethod
    def get_purchase_orders_by_owner(cls, user: AbstractUser):
        
        cls.check_owner_permission(user)
        
        return cls.get_queryset()