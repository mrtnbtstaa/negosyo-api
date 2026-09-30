from rest_framework.routers import DefaultRouter
from apps.cart.views import CartViewSet
router = DefaultRouter()

router.register(r"carts", CartViewSet, basename="carts")