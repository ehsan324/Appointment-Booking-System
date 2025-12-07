from django.urls import path
from .views import (
    ProviderProfileListView,
    ProviderProfileDetailView,
    ServiceListCreateView,
    ServiceDetailView,
    MyProviderProfileView
)

app_name = "providers"

urlpatterns = [
    #  Provider
    path("me/profile/", MyProviderProfileView.as_view(), name="my-provider-profile"),

    # Provider profiles
    path("profiles/", ProviderProfileListView.as_view(), name="provider-list"),
    path("profiles/<int:pk>/", ProviderProfileDetailView.as_view(), name="provider-detail"),

    # Services
    path("services/", ServiceListCreateView.as_view(), name="service-list-create"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
]
