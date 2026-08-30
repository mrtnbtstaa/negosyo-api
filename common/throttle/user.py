from .base import BaseUserThrottle

class UserThrottle(BaseUserThrottle):
    """
    General authenticated user throttle.

    Example:
        1000 requests/hour/user
    """

    scope = "user"


class ProfileUpdateThrottle(BaseUserThrottle):
    """
    Limits profile updates.

    Example:
        20 requests/hour/user
    """

    scope = "profile_update"


class ChangePasswordThrottle(BaseUserThrottle):
    """
    Limits password change requests.

    Example:
        5 requests/hour/user
    """

    scope = "change_password"


class NotificationThrottle(BaseUserThrottle):
    """
    Limits notification-related actions.

    Example:
        100 requests/hour/user
    """

    scope = "notifications"


class ResendVerificationThrottle(BaseUserThrottle):
    """
    Limits resend verification email requests.

    Example:
        3 requests/hour per IP
    """

    scope = "protected_resend_verification"