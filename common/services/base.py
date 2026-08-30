from __future__ import annotations

from typing import Any, ClassVar

from django.db import transaction
from django.db.models import Model

from common.exceptions.api import NotFoundException


class BaseService:
    """
    Base service for write operations.

    Services are responsible for:
    - Creating records
    - Updating records
    - Deleting records
    - Applying business logic

    Services should not handle:
    - HTTP responses
    - Serializers
    - Direct querying logic
    """

    model: ClassVar[type[Model] | None] = None
    selector: ClassVar[Any | None] = None

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @classmethod
    def validate_model(cls):
        if cls.model is None:
            raise NotImplementedError(
                f"{cls.__name__} must define a model."
            )

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def create(
        cls,
        **data: Any,
    ) -> Model:
        """
        Create a new record.
        """

        cls.validate_model()

        return cls.model.objects.create(
            **data
        )

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def update(
        cls,
        instance: Model,
        **data: Any,
    ) -> Model:
        """
        Update an existing record.
        """

        for field, value in data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.save(
            update_fields=list(data.keys())
        )

        return instance

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        instance: Model,
    ) -> None:
        """
        Delete a record.
        """

        instance.delete()