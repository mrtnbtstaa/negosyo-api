from typing import Any
from django.http import HttpResponse, JsonResponse
from django.urls import resolve
from common.cache.redis_service import RedisService
from common.constants.messages import Messages
from common.exceptions.base import BaseApiException
from common.utils.get_ip import get_client_ip
from common.exceptions import (
    ValidationException,
    ConflictException
)

class IdempotencyMiddleware:
    """
    Middleware for handling idempotent HTTP requests.

    The endpoint must explicitly opt in by setting:

        idempotency_required = True

    The client must provide:

        Idempotency-Key: <unique-key>
    """

    HEADER_NAME = "Idempotency-Key"

    DEFAULT_TTL = 300  # 5 minutes

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Any):
        # Determine whether the endpoint requires idempotency.
        if not self._requires_idempotency(request):
            return self.get_response(request)

        # Get Idempotency-Key
        key = request.headers.get(self.HEADER_NAME)

        if not key:
            return self._error_response(
                ValidationException(
                    message=Messages.IDEMPOTENCY_KEY_REQUIRED
                )
            )

        # Validate Idempotency-Key
        if not self._is_valid_key(key):
            return self._error_response(
                ValidationException(
                    message=Messages.INVALID_IDEMPOTENCY_KEY
                )
            )

        # Build Redis key
        redis_key = self._build_key(request=request, key=key)

        # Atomically acquire the idempotency key.
        #
        # True  -> this request owns the operation.
        # False -> another request already owns/completed it.
        acquired = RedisService.set_if_not_exists(
            key=redis_key,
            value={"status": "processing"},
            ttl=self.DEFAULT_TTL,
        )

        # Existing idempotency key
        if not acquired:

            stored = RedisService.get(redis_key)

            # Key disappeared between SET NX and GET.
            if stored is None:
                return self._error_response(
                    ConflictException(
                        message=Messages.IDEMPOTENCY_RETRY
                    )
                )

            # Another request is still processing.
            if stored.get("status") == "processing":
                return self._error_response(
                    ConflictException(
                        message=Messages.IDEMPOTENCY_IN_PROGRESS
                    )
                )

            # Request already completed.
            # Replay the original/old response.
            if stored.get("status") == "completed":
                return self._old_response(stored)


        # Execute the actual request.
        try:
            response = self.get_response(request)
        except Exception:
            # The request failed.
            #
            # Remove the idempotency key so the client
            # can retry the operation.
            RedisService.delete(redis_key)
            raise

        
        # Successful response
        if 200 <= response.status_code < 300:

            self._store_response(
                key=redis_key,
                response=response,
            )

        # Failed response
        # Don't permanently reserve the idempotency key.
        else:
            RedisService.delete(redis_key)

        return response

    # Determine whether endpoint requires idempotency
    def _requires_idempotency(
        self,
        request: Any,
    ) -> bool:

        match = resolve(request.path_info)

        view_func = match.func

        # DRF APIView / GenericAPIView
        view_class = getattr(
            view_func,
            "view_class",
            None,
        )

        if view_class is not None:

            return getattr(
                view_class,
                "idempotency_required",
                False,
            )

        # Function-based view
        return getattr(
            view_func,
            "idempotency_required",
            False,
        )

    # Validate Idempotency-Key
    def _is_valid_key(
        self,
        key: str,
    ) -> bool:

        """
        Validate the Idempotency-Key.

        The key must be between 16 and 255 characters.
        """
        return 16 <= len(key) <= 255

    # Build Redis key
    def _build_key(
        self,
        request: Any,
        key: str,
    ) -> str:

        """
        Build a unique Redis key.

        The same Idempotency-Key can safely be used by
        different users and different endpoints.
        """

        user_identifier = (
            self._get_user_identifier(
                request
            )
        )

        return (
            f"idempotency:"
            f"{user_identifier}:"
            f"{request.method}:"
            f"{request.path}:"
            f"{key}"
        )

    # User identifier
    def _get_user_identifier(
        self,
        request: Any,
    ) -> str:

        """
        Use the authenticated user's ID when available.

        Anonymous requests fall back to the client IP.
        """

        if (hasattr(request, "user") and request.user.is_authenticated):
            return str(request.user.pk)

        return get_client_ip(request)

    # Store response
    def _store_response(
        self,
        key: str,
        response: Any,
    ) -> None:

        """
        Store the original response so a retry can
        receive the same response.
        """

        RedisService.set(
            key=key,
            value={
                "status": "completed",
                "status_code": response.status_code,
                "content": response.content.decode(
                    "utf-8"
                ),
                "content_type": response.get(
                    "Content-Type",
                    "application/json",
                ),
            },
            ttl=self.DEFAULT_TTL,
        )

    # Replay previous response
    def _old_response(
        self,
        stored: dict[str, Any],
    ) -> HttpResponse:

        """
        Reconstruct the original HTTP response.
        """

        return HttpResponse(
            content=stored["content"],
            status=stored["status_code"],
            content_type=stored.get(
                "content_type",
                "application/json",
            ),
        )

    def _error_response(
        self,
        exception: BaseApiException,
    ) -> JsonResponse:

        payload = exception.to_dict()

        return JsonResponse(
            {
                "success": False,
                "message": payload["message"],
                "errors": payload.get("errors"),
                "meta": payload.get("meta"),
                "error_code": payload["error_code"],
            },
            status=exception.status_code,
        )

