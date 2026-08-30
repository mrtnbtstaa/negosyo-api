from __future__ import annotations

from typing import Any
from django.forms.models import model_to_dict
from apps.audit_logging.models import AuditLog
from django.conf import settings
from common.constants.audit import AuditActionEnum
from common.utils.get_ip import get_client_ip
from common.constants.excluded_fields import EXCLUDED_FIELDS, MASK_FIELDS
from common.utils.masking import mask_email
from uuid import UUID

class AuditLogService:

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    @staticmethod
    def serialize_instance(
        instance,
        *,
        exclude_fields: set[str] | None = {*EXCLUDED_FIELDS},
        mask_fields: set[str] | None = {*MASK_FIELDS},
    ) -> dict[str, Any]:

        exclude_fields = (
            set(EXCLUDED_FIELDS)
            if exclude_fields is None
            else exclude_fields
        )

        mask_fields = (
            set(MASK_FIELDS)
            if mask_fields is None
            else mask_fields
        )

        # Convert model to dictionary
        data = model_to_dict(
            instance,
            exclude=exclude_fields,
        )

        serialized = {}

        for field, value in data.items():

            value = AuditLogService._serialize_value(value)

            if field in mask_fields:
                value = AuditLogService._mask_value(field, value)

            serialized[field] = value

        return serialized

    # ---------------------------------------------------------
    # Value Serialization
    # ---------------------------------------------------------

    @staticmethod
    def _serialize_value(
        value: Any,
    ) -> Any:

        if value is None:
            return None

        if isinstance(value, UUID):
            return str(value)

        if hasattr(value, "isoformat"):
            return value.isoformat()

        if hasattr(value, "pk"):
            return str(value.pk)

        if isinstance(value, (list, tuple)):
            return [
                AuditLogService._serialize_value(item)
                for item in value
            ]

        if isinstance(value, dict):
            return {
                key: AuditLogService._serialize_value(item)
                for key, item in value.items()
            }

        return value

    # ---------------------------------------------------------
    # Diff
    # ---------------------------------------------------------

    @staticmethod
    def diff(
        original: dict[str, Any],
        current: dict[str, Any],
    ) -> dict[str, Any]:

        changes = {}

        fields = set(original) | set(current)

        for field in fields:

            old_value = original.get(field)
            new_value = current.get(field)

            if old_value == new_value:
                continue

            changes[field] = {
                # "old": old_value,
                "new": new_value,
            }

        return changes

    # ---------------------------------------------------------
    # Create Audit Log
    # ---------------------------------------------------------

    @staticmethod
    def log(
        *,
        audit_action: AuditActionEnum = AuditActionEnum.CREATE,
        request,
        action: str,
        instance=None,
        original: dict[str, Any] | None = None,
        changes: dict[str, Any] | None = None,
        exclude_fields: set[str] | None = {*EXCLUDED_FIELDS},
    ) -> AuditLog | None:

        if not settings.AUDIT_LOGGING.get(audit_action, False):
            return None

        exclude_fields = exclude_fields or set()

        user = (
            request.user
            if request.user.is_authenticated
            else None
        )

        model_name = None

        if instance is not None:
            model_name = instance.__class__.__name__

        if original is not None:
            original = {
                field: value
                for field, value in original.items()
                if field not in exclude_fields
            }

        if changes is not None:
            changes = {
                field: value
                for field, value in changes.items()
                if field not in exclude_fields
            }


        return AuditLog.objects.create(
            user=user,
            action=action,
            module_name=str(model_name) if model_name else "Anonymous",
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT"),
            original=original,
            changes=changes,
        )

    @staticmethod
    def _mask_value(
        field: str,
        value: Any,
    ) -> Any:

        if field == "email" and isinstance(value, str):
            return mask_email(value)

        return value