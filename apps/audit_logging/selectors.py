from common.selectors.base import BaseSelector
from .models import AuditLog

class AuditLoggingSelector(BaseSelector):

    model = AuditLog
