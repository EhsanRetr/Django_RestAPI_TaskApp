from rest_framework import viewsets,status,filters
from .models import House
from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrReadonly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsHouseManagerOrReadonly,]
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields=['name','discription',]
    ordering_fields=['points','complated_tasks_count','notcomplated_tasks_count',]
    filterset_fields=['members',]




    @action(detail=True,methods=['post'],name='Join',permission_classes=[])
    def join(self,request,pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if (user_profile.house == None):
                user_profile.house = house
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif (user_profile in house.members.all()):
                return Response({"detail":"already a member in this house"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail":"already a member in another house"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



    @action(detail=True,methods=['post'],name='leave',permission_classes=[])
    def leave(self,request,pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if (user_profile in house.members.all()):
                user_profile.house = None
                user_profile.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail":"already a member in the house"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    @action(detail=True,methods=['post'],name='remove-member',)
    def remove_member(self,request,pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get('user_id',None)
            if (user_id == None):
                return Response({"user_id":"not provided"},status=status.HTTP_400_BAD_REQUEST)
            user_profile = User.objects.get(pk=user_id).profile
            hous_members = house.members
            if (user_profile in hous_members.all()):
                hous_members.remove(user_profile)
                house.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail":"already a member in the house"},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as e:
            return Response({"detail":"the user_id is not exist"},status=status.HTTP_400_BAD_REQUEST)