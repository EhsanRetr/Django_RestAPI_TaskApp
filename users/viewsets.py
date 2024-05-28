from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerilizer
from rest_framework import viewsets, mixins
from .permissions import IsUserOwnerOrPostOnly, IsProfileOwnerOrReadOnly
from .models import Profile

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrPostOnly,]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.UpdateModelMixin):
    permission_classes = [IsProfileOwnerOrReadOnly,]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerilizer
    