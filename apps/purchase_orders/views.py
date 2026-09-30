from common.views.api import ProtectedBaseAPiView
from common.views.viewsets import BaseModelViewSet
from .selectors import PurchaseOrderSelector
from .models import PurchaseOrderChoices
from common.permission import IsOwnerPermission
from .serializers import (
    CreatePurchaseOrderSerializer,
    PurchaseOrderSerializer,
    DetailPurchaseOrderSerializer,
    PurchaseOrderSummarySerializer
)
from common.constants.messages import Messages
from common.responses.success import OkResponse
from rest_framework.decorators import action
from .models import PurchaseOrder
from django.db.models import Count, Q, Sum

class PurchaseOrderViewSet(BaseModelViewSet, ProtectedBaseAPiView):
    
    selector = PurchaseOrderSelector
    
    serializer_action_classes = {
        "create": CreatePurchaseOrderSerializer,
        "list": PurchaseOrderSerializer,
        "retrieve": DetailPurchaseOrderSerializer,
        "update": CreatePurchaseOrderSerializer,
        "partial_update": CreatePurchaseOrderSerializer,
        "summary": PurchaseOrderSummarySerializer
    }
    
    @action(detail=True, methods=["PATCH"], permission_classes=[IsOwnerPermission])
    def delivered(self, request, pk=None):
        
        order = self.get_object() # Fetches the purchase order using the standard ID
        order.status = PurchaseOrderChoices.DELIVERED.value
        order.save(update_fields=["status"])
        return OkResponse(message=Messages.UPDATED)
    
    @action(detail=False, methods=["GET"], permission_classes=[IsOwnerPermission])
    def summary(self, request):
        
        business = getattr(request.user, "owned_business", None)
        
        order_summary = (
            PurchaseOrder
            .objects
            .filter(business=business)
            .aggregate(
                total_order=Count("id"),
                total_transit=Count("id", filter=Q(status="in transit")),
                total_delivered=Count("id", filter=Q(status="delivered")),
                total_procurement=Sum("total_amount")
            )
        )
        
        serializer = self.get_serializer(order_summary)
        
        return OkResponse(
            message=Messages.OK,
            data=serializer.data
        )
    
    def perform_create(self, serializer):
        self.selector.check_owner_permission(self.request.user)
        business = getattr(self.request.user, "owned_business", None)
        serializer.save(
            business=business,
            status="pending"
        )
            
    def get_queryset(self):
        return self.selector.get_purchase_orders_by_owner(self.request.user)
