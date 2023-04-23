from rest_framework import permissions
from rest_framework import viewsets

from .permissions import IsOwnerOrReadOnly
from .models import TaskList,Task
from .serializers import TaskListSerializer,TaskSerializer


# Create your views here.

class ListViewSet(viewsets.ModelViewSet):
	permission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly
	)
	
	serializer_class = TaskListSerializer
	queryset = TaskList.objects.all()
	
	def perform_create(self,serializer):
		serializer.save(user = self.request.user)
	
	def get_queryset(self):
		return self.queryset.filter(user = self.request.user)
	
	
	
	


class TaskViewSet(viewsets.ModelViewSet):
	permission_classes = (
		permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly
	)
	
	serializer_class = TaskSerializer
	queryset = Task.objects.all()
	
	def perform_create(self,serializer):
		serializer.save(user = self.request.user)
	
	def get_queryset(self):
		return self.queryset.filter(user = self.request.user)
	





	