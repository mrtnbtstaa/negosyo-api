from rest_framework.permissions import BasePermission
from common.exceptions.api import PermissionDeniedException
from common.constants.messages import Messages

class IsOwnerPermission(BasePermission):
    
    def has_permission(self, request, view):
        if getattr(request.user, "account_type", None) == "owner":
            return True
        raise PermissionDeniedException(message=Messages.FORBIDDEN)
    
class IsCustomerPermission(BasePermission):
    
    def has_permission(self, request, view):
        if getattr(request.user, "account_type", None) == "customer":
            return True
        raise PermissionDeniedException(message=Messages.FORBIDDEN)
    
class IsOwnerAndCustomerPermission(BasePermission):
    
    def has_permission(self, request, view):
        if getattr(request.user, "account_type", None) == "owner":
            return True
        if getattr(request.user, "account_type", None) == "customer":
            return True
        raise PermissionDeniedException(message=Messages.FORBIDDEN)
    
