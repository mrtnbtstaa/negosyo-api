from rest_framework.routers import DefaultRouter
from apps.product_stock.views import ProductStockViewSet

router = DefaultRouter()

router.register(r"product-stock", ProductStockViewSet, basename="product-stock")