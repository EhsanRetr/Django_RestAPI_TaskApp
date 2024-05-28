from django.db import models
import uuid
import os
from django.utils.deconstruct import deconstructible
# Create your models here.
NOT_COMPLETE = 'NOT_COMPLETE'
COMPLETE = 'COMPLETE'
TASK_STATUS_CHOICES =[
    ('NOT_COMPLETE','not completed'),
    ('COMPLETE','complete'),
]
@deconstructible
class GenerateAttachmentPath(object):
    def __str__(self):
        pass
    def __call__(self,instance, filename):
        ext = filename.split('.')[-1]
        path =f'media/tasks/{instance.task.id}/attachment'
        name = f'{instance.id}.{ext}'
        return os.path.join(path,name)
    
attachment_file_path = GenerateAttachmentPath()

class TaskList(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey('users.Profile',null=True,blank=True,on_delete=models.SET_NULL,related_name='created_tasks_list')
    house = models.ForeignKey('home.House',on_delete=models.CASCADE,related_name='lists')
    name = models.CharField(max_length=120)
    discription = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=12,choices=TASK_STATUS_CHOICES,default=NOT_COMPLETE)
    def __str__(self):
        return f'{self.id} | {self.name}'

class Task(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True,blank=True)
    created_by = models.ForeignKey('users.Profile',null=True,blank=True,on_delete=models.SET_NULL,related_name='created_tasks')
    completed_by =models.ForeignKey('users.Profile',null=True,blank=True,on_delete=models.SET_NULL,related_name='completed_tasks')
    task_list = models.ForeignKey('Task.TaskList',on_delete=models.CASCADE,related_name='tasks')
    name = models.CharField(max_length=120)
    discription = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=12,choices=TASK_STATUS_CHOICES,default=NOT_COMPLETE)
    def __str__(self):
        return f'{self.id} | {self.name}'

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=attachment_file_path)
    task = models.ForeignKey('Task.Task',on_delete=models.CASCADE,related_name='attachments')
    def __str__(self):
        return f'{self.id} | {self.task}'
