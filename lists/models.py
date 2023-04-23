import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

# Create your models here.

User = get_user_model()


class TaskList(models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(_('list name'),max_length = 120)
	timestamp = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return self.name
	


class Task(models.Model):
	id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	title = models.CharField(_('title'), max_length = 200)
	description = models.TextField(_('description'), max_length = 1000, null = True, blank = True)
	
	
	def __str__(self):
		return self.title