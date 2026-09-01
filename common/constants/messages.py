class Messages:

    def __new__(cls):
        raise TypeError("Messages cannot be instantiated.")

    OK = "Request completed successfully."

    CREATED = "Resource created successfully."

    UPDATED = "Resource updated successfully."

    DELETED = "Resource deleted successfully."

    RETRIEVED = "Resource retrieved successfully."

    VALIDATION_FAILED = "Validation failed."

    BAD_REQUEST = "Bad request."

    JSON_ERROR = "Invalid json format provided"

    UNAUTHORIZED = "Authentication credentials were not provided."

    FORBIDDEN = "You do not have permission to perform this action."

    NOT_FOUND = "Resource not found."

    CONFLICT = "Conflict resource detected."

    TOO_MANY_REQUESTS = "Too many requests."

    INTERNAL_SERVER_ERROR = "Internal server error."

    UNEXPECTED_ERROR = "Unexpected error."

    BUSINESS_VIOLATED = "Business rule violated."

    PERMISSION_DENIED = "You do not have permission to access this resource."

    AUTHENTICATION_FAILED = "Authentication credentials were not valid."

    AUTHENTICATION_EXPIRED = "Your session has expired. Please log in again."

    LOGOUT_SUCCESS = "Successfully logged out."

    LOGIN_SUCCESS = "Successfully logged in."

    INVALID_CREDENTIALS = "Invalid email or password."

    EMAIL_EXISTS = "An account with this email already exists."

    EMAIL_ALREADY_VERIFIED = "Email is already verified."

    NO_USER_FOUND = "No user found."

    EMAIL_NOT_FOUND = "No account was found with this email address."

    VERIFY_EMAIL = "Please verify your email before accessing this resource."

    EMAIL_LINK_SENT = "If an account exists with this email address, a link has been sent."

    EMAIL_VERIFIED = "Your email has been successfully verified."

    LINK_EXPIRED = "Verification link is invalid or has expired."

    TOKEN_INVALID = "The token was invalid or expired."

    TOKEN_USED = "This verification link is invalid or has expired."

    TOKEN_REVOKED = "Authentication token has been revoked."

    PASSWORD_RESET_EMAIL_SENT = "If an account exists with this email address, a password reset link has been sent."

    # Infrastructure Messages
    DATABASE_INTEGRITY = "A database integrity constraint was violated."

    PROTECTED_RESOURCE = "This resource cannot be deleted because it is referenced by other records."

    RESTRICTED_RESOURCE = "The requested operation is restricted by related resources."

    DATABASE_OPERATION = "A database operation failed."

    DATABASE_UNAVAILABLE = "The database service is temporarily unavailable."

    DATABASE_PROGRAMMING = "An internal database error occurred."

    DATABASE_DATA = "The provided data could not be processed."

    DATABASE_INTERFACE = "A database interface error occurred."
    
    DATABASE_INTERNAL = "The database encountered an internal error."

    # Idempotency
    IDEMPOTENCY_KEY_REQUIRED = "Idempotency-Key header is required."

    INVALID_IDEMPOTENCY_KEY = "The Idempotency-Key is invalid."

    IDEMPOTENCY_IN_PROGRESS = "A request with this Idempotency-Key is already being processed."

    IDEMPOTENCY_RETRY = "The request could not be completed. Please try again."

    IDEMPOTENCY_ALREADY_PROCESSED = "The request has already been processed."

    # Cloudinary

    STORAGE_REQUEST_ERROR = "The file storage request is invalid."

    STORAGE_PERMISSION_ERROR = "Unable to access file storage."

    STORAGE_OPERATION_FAILED = "Unable to complete the file storage operation."

    STORAGE_TEMPORARILY_UNAVAILABLE = "File storage service is temporarily unavailable. Please try again later."

    STORAGE_FILE_ALREADY_EXISTS = "The file already exists."