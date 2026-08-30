from __future__ import annotations
from typing import Type
from rest_framework_simplejwt.tokens import TokenError, TokenBackendError
from django.core.exceptions import PermissionDenied


from cloudinary.exceptions import (
    NotAllowed,
    AuthorizationRequired,
    BadRequest,
    RateLimited,
    AlreadyExists
)
from django.http import Http404
from django.db import (
    IntegrityError,
    DatabaseError,
    OperationalError,
    ProgrammingError,
    DataError,
    InterfaceError, 
    InternalError
)

from django.db.models.deletion import (
    ProtectedError,
    RestrictedError,
)

from rest_framework.exceptions import (
    NotAuthenticated,
    PermissionDenied as DRFPermissionDenied,
    ValidationError,
    Throttled,
    AuthenticationFailed,
    ParseError
)

from common.responses.error import ErrorResponse

from .api import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    ValidationException,
    TooManyRequestsException,
    DatabaseIntegrityException,
    ProtectedResourceException,
    RestrictedResourceException,
    DatabaseInterfaceException,
    DatabaseInternalException,
    DatabaseOperationException,
    DatabaseProgrammingException,
    DatabaseUnavailableException,
    AuthenticationExpiredException,
    TokenExpiredException,
    InvalidJsonException,
    AuthenticationFailedException,
    StoragePermissionException,
    StorageAlreadyExistsException,
    StorageAuthorizationException,
    StorageRateLimitException,
    StorageBadRequestException
)
from .base import BaseApiException


class ExceptionMapper:
    """
    Maps framework, Django, and DRF exceptions into
    standardized API responses.
    """

    EXCEPTION_MAPPER: dict[Type[Exception], Type[BaseApiException]] = {
        # HTTP
        Http404: NotFoundException,
        PermissionDenied: ForbiddenException,
        DRFPermissionDenied: ForbiddenException,
        NotAuthenticated: UnauthorizedException,
        AuthenticationFailed: AuthenticationFailedException,

        # DRF
        ValidationError: ValidationException,
        ParseError: InvalidJsonException,

        # JWT
        TokenError: TokenExpiredException,
        TokenBackendError: AuthenticationExpiredException,

        # Database
        IntegrityError: DatabaseIntegrityException,
        ProtectedError: ProtectedResourceException,
        RestrictedError: RestrictedResourceException,

        # Infrastructure
        DatabaseError: DatabaseOperationException,
        OperationalError: DatabaseUnavailableException,
        ProgrammingError: DatabaseProgrammingException,
        DataError: BadRequestException,
        InterfaceError: DatabaseInterfaceException,
        InternalError: DatabaseInternalException,

        # External Services
        NotAllowed: StoragePermissionException,
        RateLimited: StorageRateLimitException,
        AuthorizationRequired: StorageAuthorizationException,
        AlreadyExists: StorageAlreadyExistsException,
        BadRequest: StorageBadRequestException

    }

    @classmethod
    def map(cls, exc: Exception) -> ErrorResponse | None:
        """
        Convert an exception into an ErrorResponse.

        Returns None if the exception is not handled.
        """

        # ------------------------------------------
        # Already one of our exceptions
        # ------------------------------------------

        if isinstance(exc, BaseApiException):
            return ErrorResponse(exc)

        # ------------------------------------------
        # DRF ValidationError
        # ------------------------------------------

        if isinstance(exc, ValidationError):
            return ErrorResponse(
                ValidationException(
                    errors=exc.detail,
                )
            )

        if isinstance(exc, Throttled):
            return ErrorResponse(
                TooManyRequestsException(
                    meta={
                        "retry_after": exc.wait,
                        "detail": exc.detail
                    }
                )
            )

        # ------------------------------------------
        # Registry-based mapping
        # ------------------------------------------
        for source_exception, target_exception in cls.EXCEPTION_MAPPER.items():
            if isinstance(exc, source_exception):
                return ErrorResponse(target_exception())

        return None