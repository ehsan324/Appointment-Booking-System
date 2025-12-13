from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProvider(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "is_provider", False)
        )


class IsClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "is_client", False)
        )


class IsOwnerOrReadOnly(BasePermission):
    owner_attr = "user"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        owner = getattr(obj, self.owner_attr, None)
        return owner == user
