from rest_framework import routers
from .viewsets import HouseViewSet

app_name='home'

router = routers.DefaultRouter()
router.register(r'home',HouseViewSet)