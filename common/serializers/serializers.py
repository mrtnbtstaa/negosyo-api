from __future__ import annotations

from typing import ClassVar

from rest_framework.serializers import BaseSerializer


class SerializerActionMixin:

    """
    Allows mapping serializers based on ViewSet actions.

    serializer_action_classes = {
        "create": UserCreateSerializer,
        "list": UserListSerializer,
        "retrieve": UserDetailSerializer,
        "update": UserUpdateSerializer,
    }

    """

    serializer_action_classes: ClassVar[dict[str, type[BaseSerializer]]] = {}

    def get_serializer_class(self):
        """
        Return serializer based on current action.

        Falls back to default serializer_class.
        """

        action = getattr(self,"action",None)

        serializer_class = self.serializer_action_classes.get(action)

        if serializer_class:
            return serializer_class

        return super().get_serializer_class()