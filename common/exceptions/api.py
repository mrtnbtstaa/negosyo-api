from rest_framework import status
from common.constants.error_codes import ErrorCodes
from common.constants.messages import Messages
from .base import BaseApiException

class BadRequestException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = Messages.BAD_REQUEST
    default_error_code = ErrorCodes.BAD_REQUEST


class ValidationException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = Messages.VALIDATION_FAILED
    default_error_code = ErrorCodes.VALIDATION_ERROR


class UnauthorizedException(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = Messages.UNAUTHORIZED
    default_error_code = ErrorCodes.UNAUTHORIZED

class AuthenticationFailedException(UnauthorizedException):
    default_message = Messages.AUTHENTICATION_FAILED


class AuthenticationExpiredException(UnauthorizedException):
    default_message = Messages.AUTHENTICATION_EXPIRED


class TokenExpiredException(UnauthorizedException):
    default_message = Messages.TOKEN_INVALID


class ForbiddenException(BaseApiException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = Messages.FORBIDDEN
    default_error_code = ErrorCodes.FORBIDDEN


class NotFoundException(BaseApiException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = Messages.NOT_FOUND
    default_error_code = ErrorCodes.NOT_FOUND


class ConflictException(BaseApiException):
    status_code = status.HTTP_409_CONFLICT
    default_message = Messages.CONFLICT
    default_error_code = ErrorCodes.CONFLICT


class BusinessRuleException(BaseApiException):
    status_code = status.HTTP_409_CONFLICT
    default_message = Messages.BUSINESS_VIOLATED
    default_error_code = ErrorCodes.CONFLICT


class TooManyRequestsException(BaseApiException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_message = Messages.TOO_MANY_REQUESTS
    default_error_code = ErrorCodes.TOO_MANY_REQUESTS


class InvalidJsonException(BadRequestException):
    default_message = Messages.JSON_ERROR

class InternalServerErrorException(BaseApiException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = Messages.INTERNAL_SERVER_ERROR
    default_error_code = ErrorCodes.INTERNAL_SERVER_ERROR

class DatabaseIntegrityException(ConflictException):
    
    """
    Raised when a database integrity constraint is violated.
    """
    default_message = Messages.DATABASE_INTEGRITY


class ProtectedResourceException(ConflictException):
    """
    Raised when attempting to delete a resource that is
    referenced by other records.
    """
    default_message = Messages.PROTECTED_RESOURCE


class RestrictedResourceException(ConflictException):
    """
    Raised when a restricted database relationship
    prevents the requested operation.
    """
    default_message = Messages.RESTRICTED_RESOURCE        


class DatabaseOperationException(InternalServerErrorException):
    """
    Generic database failure.
    """
    default_message = Messages.DATABASE_OPERATION

class DatabaseUnavailableException(InternalServerErrorException):
    """
    Raised when the database cannot be reached or is unavailable.
    """
    default_message = Messages.DATABASE_UNAVAILABLE

class DatabaseProgrammingException(InternalServerErrorException):
    """
    Raised when an internal database programming error occurs.
    """
    default_message = Messages.DATABASE_PROGRAMMING


class DatabaseDataException(InternalServerErrorException):
    """
    Raised when invalid or incompatible data reaches the database.
    """
    default_message = Messages.DATABASE_DATA


class DatabaseInterfaceException(InternalServerErrorException):
    """
    Raised when the database driver or interface fails.
    """
    default_message = Messages.DATABASE_INTERFACE


class DatabaseInternalException(InternalServerErrorException):
    """
    Raised when the database encounters an internal failure.
    """
    default_message = Messages.DATABASE_INTERNAL


# Cloudinary exceptions

class StorageBadRequestException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = Messages.STORAGE_REQUEST_ERROR
    default_error_code = ErrorCodes.STORAGE_BAD_REQUEST

class StoragePermissionException(BaseApiException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = Messages.STORAGE_OPERATION_FAILED
    default_error_code = ErrorCodes.STORAGE_PERMISSION_ERROR

class StorageRateLimitException(BaseApiException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = Messages.STORAGE_TEMPORARILY_UNAVAILABLE
    default_error_code = ErrorCodes.STORAGE_RATE_LIMIT_ERROR

class StorageAuthorizationException(BaseApiException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = Messages.STORAGE_OPERATION_FAILED
    default_error_code = ErrorCodes.STORAGE_AUTHORIZATION_ERROR

class StorageAlreadyExistsException(BaseApiException):
    status_code = status.HTTP_409_CONFLICT
    default_message = Messages.STORAGE_FILE_ALREADY_EXISTS
    default_error_code = ErrorCodes.STORAGE_ALREADY_EXISTS_ERROR