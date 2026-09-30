from common.views.viewsets import BaseModelViewSet
from common.views.api import ProtectedBaseAPiView
from .selectors import SupplierSelector
from .serializers import CreateSupplierSerializer, SupplierSerializer
from common.exceptions.api import NotFoundException
from common.constants.messages import Messages

class SupplierViewSet(BaseModelViewSet, ProtectedBaseAPiView):
    
    selector = SupplierSelector
    
    serializer_action_classes = {
        "create": CreateSupplierSerializer,
        "list": SupplierSerializer,
        "retrieve": SupplierSerializer,
        "update": SupplierSerializer,
        "partial_update": CreateSupplierSerializer
    }
    
    def get_queryset(self):
        return self.selector.get_supplier_by_owner(self.request.user)
    
    def perform_create(self, serializer):
        self.selector.check_owner_permission(self.request.user)
        owned_store = self.request.user.owned_stores.first()
        
        if owned_store is None:
            raise NotFoundException(message=Messages.NOT_FOUND)
        
        serializer.save(merchant=owned_store)