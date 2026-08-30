from __future__ import annotations
import re
from django.core.exceptions import ValidationError


# --------------------------------------------------------
# Blank / Empty
# --------------------------------------------------------

def validate_not_blank(value: str) -> None:
    """
    Reject empty or whitespace-only strings.
    """

    if value is None:
        raise ValidationError("This field is required.")

    if not value.strip():
        raise ValidationError("This field cannot be blank.")


# --------------------------------------------------------
# Whitespace
# --------------------------------------------------------

def validate_no_leading_trailing_spaces(value: str) -> None:
    """
    Reject values with leading or trailing spaces.
    """

    if value != value.strip():
        raise ValidationError(
            "Leading or trailing spaces are not allowed."
        )


def validate_single_spaces(value: str) -> None:
    """
    Reject multiple consecutive spaces.
    """

    if "  " in value:
        raise ValidationError(
            "Multiple consecutive spaces are not allowed."
        )


# --------------------------------------------------------
# Characters
# --------------------------------------------------------

def validate_alpha(value: str) -> None:
    """
    Letters only.
    """

    if not value.isalpha():
        raise ValidationError(
            "Only alphabetic characters are allowed."
        )


def validate_alpha_spaces(value: str) -> None:
    """
    Letters and spaces only.
    """

    if not re.fullmatch(r"[A-Za-z ]+", value):
        raise ValidationError(
            "Only letters and spaces are allowed."
        )


def validate_alphanumeric(value: str) -> None:
    """
    Letters and numbers only.
    """

    if not value.isalnum():
        raise ValidationError(
            "Only letters and numbers are allowed."
        )


def validate_alphanumeric_spaces(value: str) -> None:
    """
    Letters, numbers and spaces.
    """

    if not re.fullmatch(r"[A-Za-z0-9 ]+", value):
        raise ValidationError(
            "Only letters, numbers and spaces are allowed."
        )


# --------------------------------------------------------
# Username
# --------------------------------------------------------

USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_.]+$")


def validate_username(value: str) -> None:
    """
    Username validator.

    Allowed:
        john
        john123
        john_doe
        john.doe
    """

    if not USERNAME_REGEX.fullmatch(value):
        raise ValidationError(
            "Username may only contain letters, numbers, underscores, and periods."
        )


# --------------------------------------------------------
# Slug
# --------------------------------------------------------

SLUG_REGEX = re.compile(r"^[a-z0-9-]+$")


def validate_slug(value: str) -> None:
    """
    Valid slug.

    Example:
        my-scholarship
    """

    if not SLUG_REGEX.fullmatch(value):
        raise ValidationError(
            "Invalid slug format."
        )


# --------------------------------------------------------
# Safe Text
# --------------------------------------------------------

HTML_REGEX = re.compile(r"<[^>]+>")


def validate_no_html(value: str) -> None:
    """
    Prevent HTML tags.
    """

    if HTML_REGEX.search(value):
        raise ValidationError(
            "HTML tags are not allowed."
        )


SCRIPT_REGEX = re.compile(
    r"<script.*?>.*?</script>",
    re.IGNORECASE,
)


def validate_no_script(value: str) -> None:
    """
    Prevent script tags.
    """

    if SCRIPT_REGEX.search(value):
        raise ValidationError(
            "Script tags are not allowed."
        )


# --------------------------------------------------------
# SQL Keywords
# --------------------------------------------------------

SQL_REGEX = re.compile(
    r"\b(select|insert|update|delete|drop|truncate)\b",
    re.IGNORECASE,
)


def validate_no_sql_keywords(value: str) -> None:
    """
    Basic SQL keyword detection.

    NOTE:
    This is NOT SQL injection protection.
    Django ORM already protects against SQL injection.

    This validator simply blocks suspicious input.
    """

    if SQL_REGEX.search(value):
        raise ValidationError(
            "Suspicious input detected."
        )


# --------------------------------------------------------
# Printable Characters
# --------------------------------------------------------

def validate_printable(value: str) -> None:
    """
    Reject control characters.
    """

    if not value.isprintable():
        raise ValidationError(
            "Only printable characters are allowed."
        )


# --------------------------------------------------------
# ASCII
# --------------------------------------------------------

def validate_ascii(value: str) -> None:
    """
    ASCII characters only.
    """

    try:
        value.encode("ascii")
    except UnicodeEncodeError:
        raise ValidationError(
            "Only ASCII characters are allowed."
        )


# --------------------------------------------------------
# Reserved Words
# --------------------------------------------------------

RESERVED_WORDS = {
    "admin",
    "administrator",
    "root",
    "system",
    "superuser",
}


def validate_not_reserved(value: str) -> None:
    """
    Reject reserved words.
    """

    if value.lower() in RESERVED_WORDS:
        raise ValidationError(
            "This value is reserved."
        )


# --------------------------------------------------------
# Generic Safe Text
# --------------------------------------------------------

def validate_safe_text(value: str) -> None:
    """
    Combines commonly used validators.

    Recommended for:
        Scholarship title
        Category
        School
        Program
        Course
    """

    validate_not_blank(value)
    validate_no_html(value)
    validate_no_script(value)
    validate_printable(value)