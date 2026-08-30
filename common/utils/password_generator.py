import secrets
import string


UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"


def generate_password(length: int = 20) -> str:
    """
    Generate a cryptographically secure random password.

    The generated password contains at least:
    - 1 uppercase letter
    - 1 lowercase letter
    - 1 digit
    - 1 symbol
    """

    if length < 4:
        raise ValueError("Password length must be at least 4.")

    character_sets = (
        UPPERCASE,
        LOWERCASE,
        DIGITS,
        SYMBOLS,
    )

    # Guarantee one character from every required category.
    password = [
        secrets.choice(characters)
        for characters in character_sets
    ]

    all_characters = "".join(character_sets)

    # Fill the remaining length.
    password.extend(
        secrets.choice(all_characters)
        for _ in range(length - len(password))
    )

    # Cryptographically secure Fisher-Yates shuffle.
    for i in range(len(password) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    return "".join(password)