"""Permissions.py."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Defines a custom permission class."""

    def has_permission(self, request, view):
        """Start method checking the HTTP request."""
        return (request.method in SAFE_METHODS
                or request.user and request.user.is_staff)


class IsAuthorOrReadOnly(BasePermission):
    """Defines a custom permission class."""

    def has_permission(self, request, view):
        """Start method checking the HTTP request."""
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Return value that indicates the user has an object permission."""
        return (obj.author == request.user
                if request.method != "DELETE"
                else True)
