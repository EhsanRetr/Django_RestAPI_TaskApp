from .serializers import TaskListSerializer, AttachmentSerializer , TaskSerializer
from .models import TaskList, Task,Attachment,NOT_COMPLETE,COMPLETE
from rest_framework import viewsets, mixins, response,filters
from rest_framework import status as s
from .permissions import TaskListPermission, TaskPermissions,AttachmentPermission
from rest_framework.decorators import action
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend




class TaskListViewSet(viewsets.ModelViewSet,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [TaskListPermission,]




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes=[TaskPermissions,]
    filter_backends=[DjangoFilterBackend,filters.SearchFilter]
    filterset_fields=['status',]
    search_fields=['name','status','discription',]





    def get_queryset(self):
        queryset = super(TaskViewSet, self).get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset
    

    @action(detail=True,methods=['patch'])
    def update_task_status(self,request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            status = request.data['status']
            if (status == NOT_COMPLETE):
                if (task.status == COMPLETE):
                    task.status == NOT_COMPLETE
                    task.completed_on = None
                    task.completed_by = None
                else:
                    raise Exception("Task is already marks as not completed")
            elif(status == COMPLETE):
                if (task.status == NOT_COMPLETE):
                    task.status = COMPLETE
                    task.completed_on = timezone.now()
                    task.completed_by = profile
                else:
                    raise Exception("Task already completed")
            else:
                raise Exception("incorrect status provided")
            task.save()
            serializer = TaskSerializer(instance=task,context={'request':request})
            return response.Response(serializer.data, status=s.HTTP_200_OK)
        except Exception as e:
            return response.Response({'detail':str(e)},status=s.HTTP_400_BAD_REQUEST)


class AttachmentViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [AttachmentPermission]



