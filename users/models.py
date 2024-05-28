from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.deconstruct import deconstructible
# Create your models here.

"""
the path class for saving images in the directory 

evnen the cloud or another base for 

saving them you can customiz them so easy
"""


# this class can add the media in to the specific locaton you want

@deconstructible
class GProfileImageP(object):
    def __init__(self):
        pass
    def __call__(self,instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.user.id}/images/'
        name = f'profile_name.{ext}'
        return os.path.join(path, name)
user_instance_generate_path =GProfileImageP()


## Profile photo for the on by on user and its make by here self with signals.py just we write
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_instance_generate_path,blank=True,null=True)
    house= models.ForeignKey('home.House',on_delete=models.SET_NULL,null=True,blank=True,related_name='members')
    def __str__(self):
        return f'{self.user.username}\'s Profile'