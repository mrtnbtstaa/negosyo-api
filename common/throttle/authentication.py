from .base import BaseAnonymousThrottle

class LoginThrottle(BaseAnonymousThrottle):
    """
    Limits login attempts.

    Example:
        5 attempts/minute per IP
    """

    scope = "login"


class RegisterThrottle(BaseAnonymousThrottle):
    """
    Limits account creation attempts.

    Example:
        5 registrations/hour per IP
    """

    scope = "register"


class ForgotPasswordThrottle(BaseAnonymousThrottle):
    """
    Limits password reset requests.

    Example:
        3 requests/hour per IP
    """

    scope = "forgot_password"


class ResetPasswordThrottle(BaseAnonymousThrottle):
    """
    Limits password reset confirmation attempts.

    Example:
        10 attempts/hour per IP
    """

    scope = "reset_password"


class VerifyEmailThrottle(BaseAnonymousThrottle):
    """
    Limits email verification attempts.

    Example:
        10 attempts/hour per IP
    """

    scope = "verify_email"


class ResendVerificationThrottle(BaseAnonymousThrottle):
    """
    Limits resend verification email requests.

    Example:
        3 requests/hour per IP
    """

    scope = "public_resend_verification"