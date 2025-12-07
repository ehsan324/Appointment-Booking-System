from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProvider(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'is_provider', False)
        )

class IsProviderOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "is_provider", False)
        )


class IsServiceOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not (user and user.is_authenticated and getattr(user, "is_provider", False)):
            return False

        return obj.provider.user_id == user.id
