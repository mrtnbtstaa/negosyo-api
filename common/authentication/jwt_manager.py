from __future__ import annotations
import time
from common.cache.redis_service import RedisService
from rest_framework_simplejwt.tokens import (
    AccessToken,
    RefreshToken,
)


class JWTManager:
    """
    JWT utility class.

    Responsible for:
    - Creating tokens
    - Extracting token data
    - Managing token expiration

    """

    def __new__(cls):
        return TypeError("JWTManager cannot be instantiated.")


    @classmethod
    def create_tokens(cls, user):
        """
        Generate access and refresh tokens.

        Returns:
            {
                "access": "...",
                "refresh": "..."
            }
        """

        refresh = RefreshToken.for_user(user)

        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }


    @classmethod
    def create_access_token(cls, user):
        """
        Generate access token only.
        """

        refresh = RefreshToken.for_user(user)

        return str(
            refresh.access_token
        )


    @classmethod
    def create_refresh_token(cls, user):
        """
        Generate refresh token only.
        """

        refresh = RefreshToken.for_user(user)

        refresh["email"] = user.email

        return refresh


    @classmethod
    def decode_token(cls, token: str):
        """
        Decode JWT payload.

        Raises:
            TokenError
            if invalid.
        """

        access_token = AccessToken(
            token
        )

        return access_token.payload

    @classmethod
    def blacklist(cls, refresh_token: str) -> None:

        """
            Blacklist refresh token
        """

        RefreshToken(refresh_token).blacklist()


