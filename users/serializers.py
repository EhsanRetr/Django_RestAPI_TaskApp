
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile




"""
the Profile serializer thats connected to the User Serializer as well 
"""
class ProfileSerilizer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, many=False,view_name='user-detail')
    class Meta:
        model= Profile
        fields= ['url','id','user','image',]



"""
the User model serilizer provide the profile model too 
and the old password and new password function as well
the permission of old password for each request method 
"""
class UserSerializer(serializers.ModelSerializer):

    # in here we add all the fields we provide in to the serializer functions as well 
    password = serializers.CharField(write_only=True,required=False)
    old_password = serializers.CharField(write_only=True,required=False) #from old_password
    username = serializers.CharField(read_only=True)
    profile = ProfileSerilizer(read_only=True)



    # this validata function is for validating old password for every request method like PUT or PATCH method 
    def validate(self, data):
        request_method = self.context['request'].method
        password = data.get('password',None)
        if request_method == 'POST':
            if password == None:
                raise serializers.ValidationError({'info':"pleas provide a password"})
        elif request_method == 'PUT' or request_method == 'PATCH':
            old_password = data.get('old_password', None)
            if password != None and old_password == None:
                raise serializers.ValidationError({"info":"please provide the old Password"})
        return data




    # when the user want to create a new user with a password
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    



    # checking the old_password and set the new password validated as well
    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop("password")
                old_password = validated_data.pop("old_password")
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception({"info":"Old password is incorrect"})
                user.save()
        except Exception as err:
            raise serializers.ValidationError(err)
        return super(UserSerializer, self).update(instance, validated_data)
    


    # the base serializer (model and Fields)
    class Meta:
        model= User
        fields = ["url","id","username","first_name","last_name","email","password","old_password","profile"]


