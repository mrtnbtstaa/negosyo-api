from .models import Customer
from django.contrib.auth import get_user_model
from apps.users.selectors import UserSelector
from common.constants.messages import Messages
from common.exceptions.api import ConflictException

User = get_user_model()

class CustomerService:

    def __new__(cls):
        raise TypeError("CustomerService cannot be instantiated.")

    @classmethod
    def create_customer(cls, *, full_name: str, email: str, password: str) -> None:

        if UserSelector.exists(email=email):
            raise ConflictException(errors={
                "email": [Messages.EMAIL_EXISTS]
            })

        user = User.objects.create_user(
            full_name=full_name,
            email=email,
            password=password
        )

        Customer.objects.create(user=user)

