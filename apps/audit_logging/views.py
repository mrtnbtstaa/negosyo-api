from common.views.viewsets import BaseModelViewSet
from .selectors import AuditLoggingSelector

class AuditLoggingViewSet(BaseModelViewSet):

    selector = AuditLoggingSelector

    serializer_action_classes = {

}