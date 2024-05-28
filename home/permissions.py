from rest_framework import permissions

class IsHouseManagerOrReadonly(permissions.BasePermission):
    def has_permission(self,request, View):
        if request.method is permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    def has_object_permission(self, request, View, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile == obj.manager