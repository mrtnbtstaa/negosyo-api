from django.urls import path
from .views import (
    RegisterView, 
    LoginView,
    LogoutView,
    RefreshView,
    VerifyTokenView,
    ChangePasswordView,
    ForgotPasswordView,
    VerifyEmailView,
    ResendEmailVerificationViewSet,
    ResetPasswordView,
    MeView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh-token"),
    path("verify/", VerifyTokenView.as_view(), name="verify-token"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendEmailVerificationViewSet.as_view(), name="verification-email"),
    path("me/", MeView.as_view(), name="profile-me")
]