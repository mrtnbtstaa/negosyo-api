from rest_framework.routers import DefaultRouter
from apps.users.views import UsersViewSet

router = DefaultRouter()

router.register(r"users", UsersViewSet, basename="users")