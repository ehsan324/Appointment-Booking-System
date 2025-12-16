from django.contrib import admin
from django.urls import path, include
from core.views import HealthCheckView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)



urlpatterns = [
    path('admin/', admin.site.urls),


    path('auth/', include('accounts.urls')),
    path('providers/', include('providers.urls')),
    path('bookings/', include('bookings.urls')),

    #health
    path("health/", HealthCheckView.as_view(), name="health-check"),

    #API docs
path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

]
