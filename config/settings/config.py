from decouple import config
from common.constants.audit import AuditActionEnum

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_USE_TLS = config("EMAIL_USE_TLS")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
EMAIL_API_URL = config("EMAIL_API_URL")

# 2 minutes expiration
PASSWORD_RESET_TIMEOUT = 120

IDEMPOTENCY_TTL = 600 # 10 minutes

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Template api configuration
WITH_EMAIL_VERIFICATION = False # Set to True to require email verification via Gmail; set to False to skip sending verification emails.
ENABLE_SOFT_DELETE = False # Set to True to enable soft delete functionality across models, or False to keep hard deletes. 

AUDIT_LOGGING = {
    # CRUD Audit Configuration
    AuditActionEnum.CREATE: True,
    AuditActionEnum.READ: False,
    AuditActionEnum.UPDATE: True,
    AuditActionEnum.DELETE: True,

    # Authentication Audit Configuration
    AuditActionEnum.LOGIN: True,
    AuditActionEnum.LOGOUT: True,
    AuditActionEnum.LOGIN_FALED: True,

    # Account Audit Configuration
    AuditActionEnum.REGISTER: True,
    AuditActionEnum.PASSWORD_CHANGE: True,
    AuditActionEnum.PASSWORD_RESET: True,
    AuditActionEnum.EMAIL_VERIFICATION: True,
}

SEARCH_PARAM = "search"

ORDERING_PARAM = "ordering"