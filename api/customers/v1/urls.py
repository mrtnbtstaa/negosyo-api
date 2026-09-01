from django.urls import include, path

urlpatterns = [
    path("customers/", include("apps.customers.urls")),
]   