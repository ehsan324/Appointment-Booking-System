from django.contrib import admin
from django.urls import path, include
from core.views import HealthCheckView


urlpatterns = [
    path('admin/', admin.site.urls),


    path('auth/', include('accounts.urls')),
    path('providers/', include('providers.urls')),
    path('bookings/', include('bookings.urls')),

    path("health/", HealthCheckView.as_view(), name="health-check"),

]
