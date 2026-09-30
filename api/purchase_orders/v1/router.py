from rest_framework.routers import DefaultRouter
from apps.purchase_orders.views import PurchaseOrderViewSet
router = DefaultRouter()

router.register(r"purchase-orders", PurchaseOrderViewSet, basename="purchase-orders")