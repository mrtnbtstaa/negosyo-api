from __future__ import annotations
from rest_framework_simplejwt.authentication import JWTAuthentication
from common.exceptions import AuthenticationFailedException
from common.constants.messages import Messages

class DefaultJWTAuthentication(
    JWTAuthentication
):
    """
    Default JWT authentication.

    Extends SimpleJWT authentication.

    Responsible for:
    - extracting token
    - validating token
    - retrieving user
    """

