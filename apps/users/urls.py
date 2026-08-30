from django.urls import path, include
from .views import (
    ResendEmailVerificationView
)

urlpatterns = [
    path("me/resend-verification/", ResendEmailVerificationView.as_view(), name="verification-email"),
]