from rest_framework.throttling import SimpleRateThrottle


class LoginAnonRateThrottle(SimpleRateThrottle):
    scope = "login_anon"

    def get_cache_key(self, request, view):
        if request.method != "POST":
            return None

        if request.user and request.user.is_authenticated:
            return None

        ident = self.get_ident(request)
        return self.cache_key + ident
