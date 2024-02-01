from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomPermission(BasePermission):
    """
    Custom permission class to allow read-only access for unauthenticated users.
    """

    def has_permission(self, request, view):
        # Allow read-only access for unauthenticated users
        return request.method in SAFE_METHODS or request.user and request.user.is_authenticated
