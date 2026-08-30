from django.urls import include, path
from .router import router

urlpatterns = [
    path("users/", include("apps.users.urls")),
    *router.urls
]   