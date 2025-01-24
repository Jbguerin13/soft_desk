from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        if hasattr(obj, 'author') and obj.author == request.user:
            return True

        if hasattr(obj, 'issue') and obj.issue.project.author == request.user:
            return True
        
        if hasattr(obj, 'project') and obj.project.author == request.user:
            return True

        return False
