"""
Application-wide error codes.

These constants are intended for frontend consumption.
Do not change existing values once they are published,
as clients may rely on them.
"""


class ErrorCodes:

    def __new__(cls):
        raise TypeError("ErrorCodes cannot be instantiated.")

    # ======================================================
    # Generic
    # ======================================================

    UNKNOWN_ERROR = "UNKNOWN_ERROR"

    BAD_REQUEST = "BAD_REQUEST"

    VALIDATION_ERROR = "VALIDATION_ERROR"

    NOT_FOUND = "NOT_FOUND"

    CONFLICT = "CONFLICT"

    FORBIDDEN = "FORBIDDEN"

    UNAUTHORIZED = "UNAUTHORIZED"

    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"

    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"

    # ======================================================
    # Authentication
    # ======================================================

    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

    INVALID_TOKEN = "INVALID_TOKEN"

    TOKEN_EXPIRED = "TOKEN_EXPIRED"

    REFRESH_TOKEN_EXPIRED = "REFRESH_TOKEN_EXPIRED"

    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"

    EMAIL_NOT_VERIFIED = "EMAIL_NOT_VERIFIED"

    PASSWORD_INCORRECT = "PASSWORD_INCORRECT"

    PASSWORD_TOO_WEAK = "PASSWORD_TOO_WEAK"

    # ======================================================
    # User
    # ======================================================

    USER_NOT_FOUND = "USER_NOT_FOUND"

    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"

    PHONE_ALREADY_EXISTS = "PHONE_ALREADY_EXISTS"

    USERNAME_ALREADY_EXISTS = "USERNAME_ALREADY_EXISTS"

    # ======================================================
    # File
    # ======================================================

    FILE_TOO_LARGE = "FILE_TOO_LARGE"

    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"

    IMAGE_TOO_LARGE = "IMAGE_TOO_LARGE"

    INVALID_IMAGE = "INVALID_IMAGE"

    # ======================================================
    # Permissions
    # ======================================================

    PERMISSION_DENIED = "PERMISSION_DENIED"

    NOT_OWNER = "NOT_OWNER"

    ROLE_NOT_ALLOWED = "ROLE_NOT_ALLOWED"

    # ======================================================
    # Resource
    # ======================================================

    RESOURCE_ALREADY_EXISTS = "RESOURCE_ALREADY_EXISTS"

    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"


    # ======================================================
    # Idempotency
    # ======================================================

    IDEMPOTENCY_KEY_REQUIRED = "IDEMPOTENCY_KEY_REQUIRED"

    INVALID_IDEMPOTENCY_KEY = "INVALID_IDEMPOTENCY_KEY"

    IDEMPOTENCY_IN_PROGRESS = "IDEMPOTENCY_IN_PROGRESS"

    IDEMPOTENCY_RETRY = "IDEMPOTENCY_RETRY"

    # ======================================================
    # Cloudinary
    # ======================================================

    STORAGE_BAD_REQUEST = "STORAGE_BAD_REQUEST"

    STORAGE_PERMISSION_ERROR = "STORAGE_PERMISSION_ERROR"

    STORAGE_RATE_LIMIT_ERROR = "STORAGE_RATE_LIMIT_ERROR"

    STORAGE_AUTHORIZATION_ERROR = "STORAGE_AUTHORIZATION_ERROR"

    STORAGE_ALREADY_EXISTS_ERROR = "STORAGE_ALREADY_EXISTS_ERROR"
    
