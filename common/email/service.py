from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.users.models import User
from common.email.email_token_generator import EmailVerificationTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from apps.users.selectors import UserSelector
from common.cache.cache_service import CacheService
from common.cache.redis_service import RedisService
from common.constants.messages import Messages
from common.exceptions.api import ConflictException


class EmailService:

    """
    Reusable email service.

    Responsible for:
    - Rendering email templates
    - Sending HTML emails
    - Generating plain-text fallback
    """

    @staticmethod
    def send(
        *,
        subject: str,
        recipient: str,
        template: str,
        context: dict | None = None,
    ) -> None:
        """
        Send an HTML email using a Django template.

        Example:
            EmailService.send(
                subject="Reset Password",
                recipient=user.email,
                template="emails/forgot_password.html",
                context={
                    "user": user,
                    "reset_url": reset_url,
                },
            )
        """

        context = context or {}

        html_message = render_to_string(
            template_name=template,
            context=context,
        )

        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
        )

        email.attach_alternative(
            html_message,
            "text/html",
        )

        email.send()


    @staticmethod
    def send_verification_link(user: User) -> None:

        token = EmailVerificationTokenGenerator().make_token(user)
        
        uid = urlsafe_base64_encode(force_bytes(user.id))

        return EmailService.send(
            subject="Verify your email",
            recipient=user.email,
            template="email_verification.html",
            context={
                "user": user,
                "verification_url": f"{settings.EMAIL_API_URL}/verify?uid={uid}&token={token}"
            }
        )

    @staticmethod
    def resend_email_verification(user: User) -> None:

        user = UserSelector.get_or_none(email=user.email)

        if user is None:
            raise NotFoundException(message=Messages.NO_USER_FOUND)

        if user.email_verified:
            raise ConflictException(message=Messages.EMAIL_ALREADY_VERIFIED)

        cache_key = f"authenticated_user:{user.email}"

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
