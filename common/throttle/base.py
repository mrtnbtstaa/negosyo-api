from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import AnonRateThrottle

class BaseUserThrottle(UserRateThrottle):
    scope = None

class BaseAnonymousThrottle(AnonRateThrottle):
    scope = None