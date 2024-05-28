from rest_framework import permissions

class IsUserOwnerOrPostOnly(permissions.BasePermission):
    """
    its a custom permission for allow only user thats want 
    register the user authenticat
    """
    def has_permission(self, request, View):
        return True
    def has_object_permission(self, request, View, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return (request.user == obj)
        return False
    
class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    this is a custom profile permission that 
    allow user edit there own profile model only 
    """
    def has_permission(self, request, View):
        return True
    def has_object_permission(self, request, View, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return request.user.profile == obj
        return False