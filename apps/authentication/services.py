from typing import Any
from apps.users.models import User
from common.exceptions import ConflictException, UnauthorizedException, BadRequestException, NotFoundException
from apps.users.selectors import UserSelector
from django.contrib.auth import authenticate, login, logout
from common.authentication.jwt_manager import JWTManager
from common.constants.messages import Messages
from common.email.service import EmailService
from common.email.email_token_generator import EmailVerificationTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from common.cache.cache_service import CacheService
from common.cache.redis_service import RedisService
from apps.profiles.services import ProfileService
from common.constants.audit import AuditActionEnum
from apps.audit_logging.services import AuditLogService
from apps.audit_logging.models import Action

class AuthenticationService:

    def __new__(cls):
        raise TypeError("AuthenticationService cannot be instantiated.")

    @staticmethod
    def register(
        *,
        email: str,
        password: str,
        profile_image=None,
        request: Any
    ) -> User:

        if UserSelector.exists(email=email):
            raise ConflictException(message=Messages.EMAIL_EXISTS)

        user = User.objects.create_user(
            email=email,
            password=password
        )

        if profile_image:
            ProfileService.create_profile(
                user,
                profile_image
            )
    
        if settings.WITH_EMAIL_VERIFICATION:
            EmailService.send_verification_link(user)

        return user


    @staticmethod
    def login(email: str, password: str, request: Any) -> dict:

        user = authenticate(request, email=email, password=password)

        if user is None:
            AuditLogService.log(
                audit_action=AuditActionEnum.LOGIN_FALED,
                request=request,
                action=Action.LOGIN_FAILED,
                instance=request.user
            )
            raise UnauthorizedException(message=Messages.INVALID_CREDENTIALS)

        if not user.email_verified and settings.WITH_EMAIL_VERIFICATION:
            raise UnauthorizedException(message=Messages.VERIFY_EMAIL)

        refresh = JWTManager.create_refresh_token(user)

        login(request, user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),   
            "user": user,
        }

    @staticmethod
    def logout(
        request: Any
    ) -> None:
        """
        Blacklist a refresh and access token.
        """ 
        JWTManager.blacklist(request.data["refresh"])

        logout(request)


    @staticmethod
    def change_password(data: dict, request: Any) -> None:
        """
            Change password user.
        """

        user = request.user

        if user is None:
            raise UnauthorizedException(message=Messages.AUTHENTICATION_EXPIRED)

        user.set_password(data["new_password"])
        user.save(update_fields=["password"])

        AuditLogService.log(
            audit_action=AuditActionEnum.PASSWORD_CHANGE,
            request=request,
            action=Action.PASSWORD_CHANGE,
            instance=user
        )

    @staticmethod
    def forgot_password(email: str) -> User:
        """
            Forgot password user
        """
        # If no email found
        if not UserSelector.exists(email=email):
            raise BadRequestException(
                message=Messages.EMAIL_NOT_FOUND
            )

        user = UserSelector.get_or_none(email=email)

        token = EmailVerificationTokenGenerator().make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.id))

        EmailService.send(
            subject="Reset your password",
            recipient=user.email,
            template="forgot_password.html",
            context={
                "user": user,
                "reset_url": f"{settings.EMAIL_API_URL}/reset-password?uid={uid}&token={token}" 
            }
        )

        return user

    @staticmethod
    def reset_password(data: dict) -> None:

        user_id = force_str(urlsafe_base64_decode(data["uid"]))

        user = UserSelector.get_or_none(id=user_id)

        if user is None:
            raise NotFoundException(message=Messages.NO_USER_FOUND)

        if not EmailVerificationTokenGenerator().check_token(user, data["token"]):
            raise UnauthorizedException(message=Messages.TOKEN_USED)

        user.set_password(data["new_password"])

        user.save(update_fields=["password"])
                

    @staticmethod
    def verify_email(uid: str, token: str) -> User:
        """
            Verify email for user
        """
        user_id = force_str(urlsafe_base64_decode(uid))

        user = UserSelector.get_or_none(id=user_id)

        if user is None:
            raise NotFoundException(message=Messages.NO_USER_FOUND)

        if not EmailVerificationTokenGenerator().check_token(user, token):
            raise UnauthorizedException(message=Messages.LINK_EXPIRED)

        if user.email_verified:
            raise ConflictException(message=Messages.EMAIL_ALREADY_VERIFIED)

        user.email_verified = True

        user.save(update_fields=["email_verified"])

        return user

    @staticmethod
    def resend_email_verification(email: str) -> None:

        user = UserSelector.get_or_none(email=email)

        if user is None:
            raise NotFoundException(message=Messages.NO_USER_FOUND)
        
        if user.email_verified:
            raise ConflictException(message=Messages.EMAIL_ALREADY_VERIFIED)
        
        cache_key = f"user_email_verification:{user.email}:"
    
        if CacheService.exists(key=cache_key):
            remaining = RedisService.ttl(cache_key)

            raise ConflictException(
                message=f"Please wait {remaining} seconds before requesting another email",
                meta={
                    "remaining_seconds": remaining
                }
            )

        EmailService.send_verification_link(user)

        CacheService.store(
            cache_key,
            value=True,
            ttl=120
        )
            
    @staticmethod
    def me(
        data: dict,
        request: Any
    ) -> User:
        """
        Return the updated user.
        """

        user = request.user

    
        if user is None:
            raise NotFoundException(message=Messages.NO_USER_FOUND)

        profile_image = data.get("profile_image", None)

        if profile_image:
            ProfileService.update_profile(user, profile_image)

        email = data.get("email", user.email)

        if email is not None:

            email = email.strip().lower()

            if email != user.email.lower():
                user.email = email
                user.email_verified = False
    
                user.save(update_fields=["email", "email_verified"])
    
                if settings.WITH_EMAIL_VERIFICATION:
                    EmailService.send_verification_link(user)

        return user      


