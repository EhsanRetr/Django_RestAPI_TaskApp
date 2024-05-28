from rest_framework import serializers
from .models import House
class HouseSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True,many=True ,view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True,many=False,view_name='profile-detail')
    tasklist = serializers.HyperlinkedRelatedField(read_only=True,many=True,view_name='tasklist-detail',source='lists')
    class Meta:
        model = House
        fields = ['url','id','name','image','created_on','discription'
                  ,'manager','points','member_count','members',
                  'complated_tasks_count','notcomplated_tasks_count','tasklist']
        read_only_fields = ['points','complated_tasks_count','notcomplated_tasks_count',]