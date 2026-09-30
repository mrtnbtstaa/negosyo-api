from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("silk/", include("silk.urls"), name="silk"),
    # -------------------- V1 API --------------------------
    path("api/v1/", include("api.authentication.v1.urls")),
    path("api/v1/", include("api.users.v1.urls")),
    path("api/v1/", include("api.customers.v1.urls")),
    path("api/v1/", include("api.merchants.v1.urls")),
    path("api/v1/", include("api.suppliers.v1.urls")),
    path("api/v1/", include("api.purchase_orders.v1.urls")),
    path("api/v1/", include("api.product_stock.v1.urls")),
    path("api/v1/", include("api.cart.v1.urls")),
    # -------------------- V1 API --------------------------
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
