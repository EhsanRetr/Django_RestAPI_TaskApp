from rest_framework import permissions



"""
    the only Task owner can access there 
    own list not any body else 
"""
class TaskListPermission(permissions.BasePermission):
    def has_permission(self,request,View):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    def has_object_permission(self,request,view,obj):
        return request.user.profile == obj.created_by

    """
    this permisssion make just Task Owner 
    can see the list of there own Tasks 
    not any of other Task
    """
class TaskPermissions(permissions.BasePermission):
    def has_permission(self,request,View):
        if not request.user.is_anonymous:
            return request.user.profile.house != None
        return False
    def has_object_permission(self,request,view,obj):
        return request.user.profile.house == obj.task_list.house
    

# same as others permissions 
class AttachmentPermission(permissions.BasePermission):
    def has_permission(self, request, View):
        if not request.user.is_anonymous:
            return request.user.profile.house != None
        return False
    def has_object_permission(self, request, View,obj):
        return request.user.profile.house == obj.task.task_list.house