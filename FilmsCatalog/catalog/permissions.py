from rest_framework.permissions import BasePermission, SAFE_METHODS

from catalog.models import TYPE_CHOICES


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
        )


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.user_type == TYPE_CHOICES[2][0])
        return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.user_type == TYPE_CHOICES[1][0])
        return False
