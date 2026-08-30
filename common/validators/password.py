from __future__ import annotations
import re
from django.core.exceptions import ValidationError

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

SPECIAL_CHARACTER_REGEX = re.compile(
    r"[!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]"
)

NUMBER_REGEX = re.compile(r"\d")

UPPERCASE_REGEX = re.compile(r"[A-Z]")

LOWERCASE_REGEX = re.compile(r"[a-z]")


COMMON_PASSWORDS = {
    "password",
    "password123",
    "12345678",
    "123456789",
    "qwerty",
    "qwerty123",
    "admin",
    "admin123",
    "administrator",
    "letmein",
    "welcome",
    "abc123",
    "11111111",
    "00000000",
    "iloveyou",
}


# ---------------------------------------------------------
# Length
# ---------------------------------------------------------

def validate_password_length(password: str) -> None:

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password must contain at least {MIN_PASSWORD_LENGTH} characters."
        )

    if len(password) > MAX_PASSWORD_LENGTH:
        raise ValidationError(
            f"Password cannot exceed {MAX_PASSWORD_LENGTH} characters."
        )


# ---------------------------------------------------------
# Uppercase
# ---------------------------------------------------------

def validate_uppercase(password: str) -> None:

    if not UPPERCASE_REGEX.search(password):
        raise ValidationError(
            "Password must contain at least one uppercase letter."
        )


# ---------------------------------------------------------
# Lowercase
# ---------------------------------------------------------

def validate_lowercase(password: str) -> None:

    if not LOWERCASE_REGEX.search(password):
        raise ValidationError(
            "Password must contain at least one lowercase letter."
        )


# ---------------------------------------------------------
# Number
# ---------------------------------------------------------

def validate_number(password: str) -> None:

    if not NUMBER_REGEX.search(password):
        raise ValidationError(
            "Password must contain at least one number."
        )


# ---------------------------------------------------------
# Special Character
# ---------------------------------------------------------

def validate_special_character(password: str) -> None:

    if not SPECIAL_CHARACTER_REGEX.search(password):
        raise ValidationError(
            "Password must contain at least one special character."
        )


# ---------------------------------------------------------
# Spaces
# ---------------------------------------------------------

def validate_no_spaces(password: str) -> None:

    if " " in password:
        raise ValidationError(
            "Password cannot contain spaces."
        )


# ---------------------------------------------------------
# Common Password
# ---------------------------------------------------------

def validate_not_common_password(password: str) -> None:

    if password.lower() in COMMON_PASSWORDS:
        raise ValidationError(
            "This password is too common."
        )


# ---------------------------------------------------------
# Repeated Characters
# ---------------------------------------------------------

def validate_repeated_characters(password: str) -> None:
    """
    Reject:

    aaaaaaaa
    11111111
    !!!!!!!!
    """

    if len(set(password)) == 1:
        raise ValidationError(
            "Password cannot consist of repeated characters."
        )


# ---------------------------------------------------------
# Sequential Characters
# ---------------------------------------------------------

SEQUENCES = [
    "0123456789",
    "123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]


def validate_sequential_characters(password: str) -> None:
    """
    Reject passwords containing obvious keyboard
    or alphabetical sequences of length 4 or more.
    """

    password_lower = password.lower()

    for sequence in SEQUENCES:

        for i in range(len(sequence) - 3):

            chunk = sequence[i:i + 4]

            if chunk in password_lower:
                raise ValidationError(
                    "Password contains sequential characters."
                )

            if chunk[::-1] in password_lower:
                raise ValidationError(
                    "Password contains sequential characters."
                )


# ---------------------------------------------------------
# Username Similarity
# ---------------------------------------------------------

def validate_not_similar_to_username(
    password: str,
    username: str,
) -> None:

    if not username:
        return

    if username.lower() in password.lower():
        raise ValidationError(
            "Password is too similar to the username."
        )


# ---------------------------------------------------------
# Email Similarity
# ---------------------------------------------------------

def validate_not_similar_to_email(
    password: str,
    email: str,
) -> None:

    if not email:
        return

    local_part = email.split("@")[0]

    if local_part.lower() in password.lower():
        raise ValidationError(
            "Password is too similar to the email."
        )


# ---------------------------------------------------------
# Confirmation
# ---------------------------------------------------------

def validate_password_confirmation(
    password: str,
    confirm_password: str,
) -> None:

    if password != confirm_password:
        raise ValidationError(
            "Passwords do not match."
        )


# ---------------------------------------------------------
# Combined Validator
# ---------------------------------------------------------

def validate_strong_password(password: str) -> None:
    """
    Recommended validator for ScholarHub.
    """

    validate_password_length(password)
    validate_uppercase(password)
    validate_lowercase(password)
    validate_number(password)
    validate_special_character(password)
    validate_no_spaces(password)
    validate_not_common_password(password)
    validate_repeated_characters(password)
    validate_sequential_characters(password)