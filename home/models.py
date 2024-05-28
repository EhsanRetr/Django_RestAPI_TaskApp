from django.db import models
import os
import uuid
from django.utils.deconstruct import deconstructible
# Create your models here.
@deconstructible
class GeneratingImagePath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/houses/{instance.id}/images'
        name = f'main.{ext}'
        return os.path.join(path, name)
image_path = GeneratingImagePath()


class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to=image_path,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    discription = models.TextField()
    manager = models.OneToOneField('users.profile',on_delete=models.SET_NULL,blank=True,null=True,related_name='managed_house')
    points = models.IntegerField(default=0)
    complated_tasks_count = models.IntegerField(default=0)
    notcomplated_tasks_count = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.name}_House {self.id}'