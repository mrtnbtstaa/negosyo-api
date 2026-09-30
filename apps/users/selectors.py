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
    
    @classmethod
    def get_user(cls, user):
        return (
            cls.get_queryset()
            .select_related("user_information")    
            .only("id", "full_name", "email", "user_information__phone_number", "user_information__gender", "user_information__date_of_birth")        
            .filter(id=user.pk)
        )
        
        




