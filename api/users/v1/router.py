from rest_framework.routers import DefaultRouter
from apps.users.views import UsersViewSet, UsersMeViewSet

router = DefaultRouter()

router.register(r"users/me", UsersMeViewSet, basename="users-me")
# router.register(r"users", UsersViewSet, basename="users")