from common.views.api import PublicBaseApiView
from .serializers import CreateCustomerSerializer
from .services import CustomerService
from common.responses.success import CreatedResponse
from common.constants.messages import Messages
from apps.authentication.serializers import RegisterSerializer

class RegisterCustomerView(PublicBaseApiView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        CustomerService.create_customer(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return CreatedResponse(
            message=Messages.CREATED
        )
