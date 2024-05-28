from rest_framework import routers
from .viewsets import TaskListViewSet,AttachmentViewSet,TaskViewSet


app_name='tasks'
router = routers.DefaultRouter()


router.register('tasklist',TaskListViewSet)
router.register('attachments',AttachmentViewSet)
router.register('tasks',TaskViewSet)