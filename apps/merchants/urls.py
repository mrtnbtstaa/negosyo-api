from django.urls import path
from .views import UpdateMerchantView

urlpatterns = [
    path("onboarding/completed/", UpdateMerchantView.as_view(), name="update_merchant_information"),
]