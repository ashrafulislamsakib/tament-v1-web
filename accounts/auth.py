from datetime import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.contrib.auth import login,logout
from accounts.serializers import UserSerializer


def api_login(request,user):
	userSerializer = UserSerializer(user)
	token, created = Token.objects.get_or_create(user=user)
	token.user.last_login = timezone.now()
	token.user.save()
	login(request,user)
	return { 'user' : userSerializer.data, 'token' : token.key }
	
	
def api_logout(request):
	tokens = Token.objects.filter(user=request.user)
	for token in tokens:
		token.delete()
	logout(request)
	return True