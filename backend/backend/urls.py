from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),


    path('auth/', include('accounts.urls')),
    path('providers/', include('providers.urls')),
    path('bookings/', include('bookings.urls')),
]
