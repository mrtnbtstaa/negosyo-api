from .views import RegisterCustomerView
from django.urls import path

urlpatterns = [
    path("register/", RegisterCustomerView.as_view(), name="register_customer"),
]   