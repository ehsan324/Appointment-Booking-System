from rest_framework import request
from rest_framework.throttling import SimpleRateThrottle

class BookingCreateRateThrottle(SimpleRateThrottle):

    scope = ['booking_create']

    def get_cache_key(self, request, view):
        if request.method != 'POST':
            return None

        user = request.user
        if not user or not user.is_authenticated:
            return None

        ident = str(user.id)
        return self.cache_key + ident