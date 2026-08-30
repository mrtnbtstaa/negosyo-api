from common.responses.success import OkResponse
from common.email.service import EmailService
from common.constants.messages import Messages
from common.views.viewsets import BaseModelViewSet
from .selectors import UserSelector
from .serializers import UserSerializer
from common.views.api import ProtectedBaseAPiView

class ResendEmailVerificationView(ProtectedBaseAPiView):

    def get(self, request):

        self.check_throttles(request)

        _ = EmailService.resend_email_verification(request.user)

        return OkResponse(message=Messages.EMAIL_LINK_SENT)


class UsersViewSet(BaseModelViewSet, ProtectedBaseAPiView):

    selector = UserSelector

    serializer_action_classes = {
        "list": UserSerializer,
        "retrieve": UserSerializer,
        "update": UserSerializer
    }

    