from common.responses.success import CreatedResponse, OkResponse
from common.constants.messages import Messages
from .services import AuthenticationService
from apps.users.serializers import UserSerializer
from common.views.api import PublicBaseApiView, ProtectedBaseAPiView
from rest_framework import generics
from common.constants.audit import AuditActionEnum
from apps.audit_logging.services import AuditLogService
from apps.audit_logging.models import Action
from django.contrib.auth import get_user_model
from django.db.models import Model
from typing import Type, ClassVar
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from .serializers import (
    RegisterSerializer, 
    LoginSerializer,
    CustomTokenRefreshSerializer,
    CustomTokenVerifySerializer,
    LogoutBlacklistSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    VerifyEmailSerializer,
    ResendVerificationSerializer,
    ResetPasswordSerializer,
    MeSerializer
)
from common.throttle.authentication import (
    LoginThrottle,
    RegisterThrottle,
    ForgotPasswordThrottle,
    ResendVerificationThrottle,
    ResetPasswordThrottle,
    VerifyEmailThrottle
)
from common.throttle.user import (
    ChangePasswordThrottle
)

User = get_user_model()

class RegisterView(PublicBaseApiView, generics.CreateAPIView):

    throttle_classes = [RegisterThrottle]

    idempotency_required = True
  
    def post(self, request):

        self.check_throttles(request)

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        created_user = AuthenticationService.register(
            email=validated_data["email"],
            password=validated_data["password"],
            profile_image=validated_data.get("profile_image", None),
            request=request
        )

        created_user.refresh_from_db()

        AuditLogService.log(
            audit_action=AuditActionEnum.REGISTER,
            request=request,
            action=Action.REGISTER,
            instance=created_user
        )

        return CreatedResponse(message=Messages.CREATED, data=UserSerializer(created_user).data)

class LoginView(TokenObtainPairView):

    throttle_classes = [LoginThrottle]

    def post(self, request):
        
        self.check_throttles(request)

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        auth_data = AuthenticationService.login(
            serializer.validated_data["email"],
            serializer.validated_data["password"],
            request
        )

        AuditLogService.log(
            audit_action=AuditActionEnum.LOGIN,
            request=request,
            action=Action.LOGIN,
            instance=auth_data["user"]
        )

        return OkResponse(
            message=Messages.LOGIN_SUCCESS, 
            data={
                "access_token": auth_data["access_token"],
                "refresh_token": auth_data["refresh_token"],
                **UserSerializer(auth_data["user"]).data
            }
        )

class LogoutView(TokenBlacklistView):

    serializer_class = LogoutBlacklistSerializer

    def post(self, request):

        self.check_throttles(request)

        AuditLogService.log(
            audit_action=AuditActionEnum.LOGOUT,
            request=request,
            action=Action.LOGOUT,
            instance=request.user
        )

        _ = AuthenticationService.logout(request)
        
        return OkResponse(message=Messages.LOGOUT_SUCCESS)

class RefreshView(TokenRefreshView):

    def post(self, request):

        self.check_throttles(request)

        serializer = CustomTokenRefreshSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return OkResponse(
            message=Messages.OK,
            data={
                "access_token": serializer.validated_data["access"],
                "refresh_token": serializer.validated_data["refresh"]
            }
        )


class VerifyTokenView(TokenVerifyView):

    def get(self, request):

        self.check_throttles(request)

        serializer = CustomTokenVerifySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return OkResponse(message=Messages.OK)


class ChangePasswordView(ProtectedBaseAPiView, generics.UpdateAPIView):

    throttle_classes = [ChangePasswordThrottle]
    idempotency_required = True

    def patch(self, request):

        self.check_throttles(request)

        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})

        serializer.is_valid(raise_exception=True)

        _ = AuthenticationService.change_password(serializer.validated_data, request)

        return OkResponse(message=Messages.UPDATED)

class ForgotPasswordView(PublicBaseApiView):

    throttle_classes = [ForgotPasswordThrottle]
    idempotency_required = True

    def post(self, request):

        self.check_throttles(request)

        serializer = ForgotPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.forgot_password(serializer.validated_data["email"])

        AuditLogService.log(
            audit_action=AuditActionEnum.FORGOT_PASSWORD,
            request=request,
            action=Action.FORGOT_PASSWORD,
            instance=user,
        )

        return OkResponse(message=Messages.PASSWORD_RESET_EMAIL_SENT)


class ResetPasswordView(PublicBaseApiView):

    throttle_classes = [ResetPasswordThrottle]
    idempotency_required = True

    def patch(self, request):

        self.check_throttles(request)

        serializer = ResetPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        _ = AuthenticationService.reset_password(serializer.validated_data)

        return OkResponse(message=Messages.UPDATED)

class VerifyEmailView(PublicBaseApiView):

    throttle_classes = [VerifyEmailThrottle]

    def post(self, request):

        self.check_throttles(request)

        serializer = VerifyEmailSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.verify_email(**serializer.validated_data)

        AuditLogService.log(
            audit_action=AuditActionEnum.EMAIL_VERIFICATION,
            request=request,
            action=Action.EMAIL_VERIFICATION,
            instance=user,
        )

        return OkResponse(message=Messages.EMAIL_VERIFIED)


class ResendEmailVerificationViewSet(PublicBaseApiView):

    throttle_classes = [ResendVerificationThrottle]

    def post(self, request):

        self.check_throttles(request)

        serializer = ResendVerificationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        AuditLogService.log(
            audit_action=AuditActionEnum.RESEND_EMAIL_VERIFICATION,
            request=request,
            action=Action.RESEND_EMAIL_VERIFICATION,
            instance=serializer.instance,
        )

        _ = AuthenticationService.resend_email_verification(serializer.validated_data["email"])

        return OkResponse(message=Messages.EMAIL_LINK_SENT)


class MeView(ProtectedBaseAPiView):

    def get(self, request):

        return OkResponse(
            message=Messages.OK,
            data=UserSerializer(request.user).data
        )

    def patch(self, request):

        serializer = MeSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        original_data = AuditLogService.serialize_instance(request.user)

        user = AuthenticationService.me(
            serializer.validated_data,
            request,
        )

        user.refresh_from_db()

        changes = AuditLogService.diff(
            original=original_data,
            current=AuditLogService.serialize_instance(user)
        )

        AuditLogService.log(
            audit_action=AuditActionEnum.UPDATE,
            request=request,
            action=Action.UPDATED,
            instance=user,
            original=original_data,
            changes=changes
        )

        return OkResponse(
            message=Messages.UPDATED,
            data=UserSerializer(user).data
        )

 



