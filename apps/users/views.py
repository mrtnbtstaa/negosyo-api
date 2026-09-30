from common.responses.success import OkResponse
from common.email.service import EmailService
from common.constants.messages import Messages
from common.views.viewsets import BaseModelViewSet
from .selectors import UserSelector
from .serializers import UserSerializer, UserMeSerializer, UpdateUserMeSerializer
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
    

class UsersMeViewSet(BaseModelViewSet, ProtectedBaseAPiView):

    selector = UserSelector
    
    serializer_action_classes = {
        "list": UserMeSerializer,
        "update": UpdateUserMeSerializer,
        "partial_update": UpdateUserMeSerializer
    }
        
    def get_queryset(self):
        return self.selector.get_user(self.request.user)
    

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return OkResponse(data=serializer.data)
    
    

    
   
    
