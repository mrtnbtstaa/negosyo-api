from __future__ import annotations
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# --------------------------------------------------------
# Disposable Email Domains
# --------------------------------------------------------
DISPOSABLE_EMAIL_DOMAINS = {
    "mailinator.com",
    "guerrillamail.com",
    "10minutemail.com",
    "tempmail.com",
    "temp-mail.org",
    "yopmail.com",
    "sharklasers.com",
    "trashmail.com",
    "getnada.com",
}


# --------------------------------------------------------
# Allowed Domains
# Leave empty to allow every domain.
# --------------------------------------------------------

ALLOWED_EMAIL_DOMAINS = set()


# --------------------------------------------------------
# Blocked Domains
# --------------------------------------------------------

BLOCKED_EMAIL_DOMAINS = set()


# --------------------------------------------------------
# Basic Email Validation
# --------------------------------------------------------

def validate_email_format(value: str) -> None:
    """
    Validate email format.
    """
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError("Enter a valid email address.")


# --------------------------------------------------------
# Normalize Email
# --------------------------------------------------------

def normalize_email(value: str) -> str:
    """
    Lowercase and strip spaces.
    """

    return value.strip().lower()


# --------------------------------------------------------
# Disposable Email
# --------------------------------------------------------

def validate_not_disposable_email(value: str) -> None:
    """
    Reject temporary email providers.
    """

    value = normalize_email(value)

    domain = value.split("@")[-1]

    if domain in DISPOSABLE_EMAIL_DOMAINS:
        raise ValidationError(
            "Disposable email addresses are not allowed."
        )


# --------------------------------------------------------
# Allowed Domains
# --------------------------------------------------------

def validate_allowed_domain(value: str) -> None:
    """
    If ALLOWED_EMAIL_DOMAINS is empty,
    allow all domains.
    """

    if not ALLOWED_EMAIL_DOMAINS:
        return

    domain = normalize_email(value).split("@")[-1]

    if domain not in ALLOWED_EMAIL_DOMAINS:
        raise ValidationError(
            "This email domain is not allowed."
        )


# --------------------------------------------------------
# Blocked Domains
# --------------------------------------------------------

def validate_blocked_domain(value: str) -> None:
    """
    Reject blocked domains.
    """

    domain = normalize_email(value).split("@")[-1]

    if domain in BLOCKED_EMAIL_DOMAINS:
        raise ValidationError(
            "This email domain is blocked."
        )


# --------------------------------------------------------
# School Email
# --------------------------------------------------------

def validate_school_email(
    value: str,
    allowed_domains: list[str],
) -> None:
    """
    Example:

    validate_school_email(
        email,
        [
            "student.mcc.edu.ph",
            "mcc.edu.ph",
        ]
    )
    """

    domain = normalize_email(value).split("@")[-1]

    if domain not in allowed_domains:
        raise ValidationError(
            "Please use your school email address."
        )


# --------------------------------------------------------
# Company Email
# --------------------------------------------------------

def validate_company_email(
    value: str,
    company_domain: str,
) -> None:

    domain = normalize_email(value).split("@")[-1]

    if domain != company_domain.lower():
        raise ValidationError(
            "Please use your company email."
        )


# --------------------------------------------------------
# Gmail Only
# --------------------------------------------------------

def validate_gmail(value: str) -> None:

    domain = normalize_email(value).split("@")[-1]

    if domain != "gmail.com":
        raise ValidationError(
            "Only Gmail addresses are accepted."
        )


# --------------------------------------------------------
# Maximum Length
# --------------------------------------------------------

def validate_email_length(value: str) -> None:

    if len(value) > 254:
        raise ValidationError(
            "Email address is too long."
        )


# --------------------------------------------------------
# Combined Validator
# --------------------------------------------------------

def validate_safe_email(value: str) -> None:
    """
    Recommended validator for registration.

    Includes:
    Format
    Length
    Disposable email
    Allowed domains
    Blocked domains
    """

    value = normalize_email(value)

    validate_email_format(value)
    validate_email_length(value)
    validate_not_disposable_email(value)
    validate_allowed_domain(value)
    validate_blocked_domain(value)