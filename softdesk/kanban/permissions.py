from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission class that grants different levels of access based on user roles.

    - Read-only access (GET, HEAD, OPTIONS) is granted to any user.
    - Write access (POST, PUT, DELETE) is granted only if:
        1. The user is the author of the resource.
        2. The user is the author of the associated issue's project.
        3. The user is the author of the associated project.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks permissions for a specific object.

        Args:
            request: The HTTP request object.
            view: The view that is handling the request.
            obj: The object being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # Allow read-only permissions for safe methods
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Check if the user is the author of the object (e.g., Project, Issue, or Comment)
        if hasattr(obj, 'author') and obj.author == request.user:
            return True

        # Check if the user is the author of the project linked to the issue
        if hasattr(obj, 'issue') and obj.issue.project.author == request.user:
            return True

        # Check if the user is the author of the project itself
        if hasattr(obj, 'project') and obj.project.author == request.user:
            return True

        # Deny access otherwise
        return False
