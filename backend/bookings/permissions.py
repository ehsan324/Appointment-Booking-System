from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProvider(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'is_provider', False)
        )

class IsClient(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'is_client', False)
        )

class IsBookingOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.client.id == request.user.id