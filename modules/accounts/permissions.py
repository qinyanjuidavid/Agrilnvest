from modules.accounts.models import RoleChoices
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUser(BasePermission):
    """
    Custom permission class to allow access to SuperUser users only.

    Methods:
        has_permission(self, request, view): Check if the
        user is authenticated.
        has_object_permission(self, request, view, obj):
        Check object-specific permissions.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check object-specific permissions.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if (
            request.user.role == RoleChoices.SUPERUSER
            and request.user.is_authenticated,
        ):
            return True
        if request.method in SAFE_METHODS:
            return True
        return False
