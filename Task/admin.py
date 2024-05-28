from django.contrib import admin
from .models import Task,TaskList,Attachment
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    pass


class TaskListAdmin(admin.ModelAdmin):
    pass



class AttachmentAdmin(admin.ModelAdmin):
    pass 


admin.site.register(Attachment,AttachmentAdmin)
admin.site.register(TaskList,TaskListAdmin)
admin.site.register(Task,TaskAdmin)