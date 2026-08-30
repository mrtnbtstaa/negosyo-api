from __future__ import annotations
from common.constants.messages import Messages
from typing import Any

from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    message = Messages.UNAUTHORIZED

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        return bool(
            request.user
            and request.user.is_authenticated
        )


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.

    Uses Django's is_staff flag.
    """

    message = "Admin permission required."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsSuperUser(BasePermission):
    """
    Allows access only to superusers.
    """

    message = "Superuser permission required."

    def has_permission(
        self,
        request,
        view,
    ) -> bool:

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwner(BasePermission):
    """
    Object-level permission.

    Requires the object to have a user field.

    Example:

        obj.user == request.user

    """

    message = Messages.PERMISSION_DENIED

    owner_field: str = "user"

    def has_object_permission(
        self,
        request,
        view,
        obj: Any,
    ) -> bool:

        if not request.user.is_authenticated:
            return False

        owner = getattr(
            obj,
            self.owner_field,
            None,
        )

        return owner == request.user


class IsEmailVerified(BasePermission):

    message = Messages.VERIFY_EMAIL

    def has_permission(self, request, view):    
        return request.user.is_authenticated and request.user.email_verified