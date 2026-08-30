from common.selectors.base import BaseSelector
from .models import User

class UserSelector(BaseSelector):

    model = User

    searchable_fields = ("email",)

    ordering_fields = ("email", "created_at")

    default_ordering = ("-created_at", )

    filterable_fields = {
        "created_at": (
            "date",
            "gte",
            "lte",
            "exact"
        ),
        "is_staff": ("exact",)
    }


