from rest_framework.routers import DefaultRouter
from apps.merchants.views import MerchantViewSet

router = DefaultRouter()

router.register(r"merchants", MerchantViewSet, basename="merchants")