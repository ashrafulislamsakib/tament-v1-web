from datetime import date, timedelta

from rest_framework import permissions,status,generics,mixins
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

#from .permissions import IsOwnerOrReadOnly
from django.utils.translation import ugettext_lazy as _
from accounts.models import SignupCode,PasswordResetCode
from accounts.auth import api_login,api_logout
from . import serializers



# Create your views here.


User = get_user_model()


class SignupAPIView(mixins.CreateModelMixin,
					generics.GenericAPIView):
	
	serializer_class = serializers.SignupSerializer
	permission_classes = (permissions.AllowAny,)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)
		
		



class LoginAPIView(APIView):
	serializer_class = serializers.LoginSerializer
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)
	def post(self,request,formate = None):
		serializer = self.serializer_class(data = request.data)
		if serializer.is_valid():
			username = serializer.data.get('username',None)
			password = serializer.data.get('password',None)
			user = authenticate(username = username,password = password)
			if user is not None and user.is_active:
				if user.is_verified or user.is_superuser:
					response = api_login(request,user)
					return Response(response)
				return Response({ 'detail' : _('your email is not varified ') })
			return Response({ 'detail' : _('unable to login with that credential')})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Logout(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	def get(self,request, format = None):
		logouted = api_logout(request)
		return Response({ 'success' : 'user logged out' })




# more auth views 
"""
	more auth views like `signup verify` ,`password change`, `password reset` and `password reset confirm`
"""


class SignupVerifyAPIView(APIView):
	serializer_class = serializers.CodeSerializer
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)
	def post(self,request, format = None):
		serializer = self.serializer_class(data = request.data)
		serializer.is_valid(raise_exception = True)
		code = serializer.data.get('code')
		verified = SignupCode.objects.set_user_is_verified(code)
		if verified:
			try:
				# delete used signup code >
				SignupCode.objects.get(code = code).delete()
			except SignupCode.DoesNotExist:
				pass
			return Response({ 'success' : 'user email verified ' })
		return Response({ 'detail' : 'incorrect code !' })
		






class PasswordChangeAPIView(APIView):
	serializer_class = serializers.PasswordChangeSerializer
	permission_classes = (permissions.IsAuthenticated,)
	"""
	To do : first check previous password then allow for new password
	"""
	def post(self, request, format = None):
		serializer = self.serializer_class(data = request.data)
		serializer.is_valid(raise_exception = True)
		password = serializer.data.get('password')
		request.user.set_password(password)
		request.user.save()
		return Response({ 'success' : 'password change was successful ' })
		




class PasswordResetAPIView(APIView):
	serializer_class = serializers.PasswordResetSerializer
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)
	def post(self, request, format = None):
		serializer = self.serializer_class(data = request.data)
		serializer.is_valid(raise_exception = True)
		email = serializer.data.get('email')
		try:
			user = User.objects.get(email=email)
			# delete all unused password rest codes
			PasswordResetCode.objects.filter(user=user).delete()
			if user.is_verified and user.is_active:
				password_reset_code  = PasswordResetCode.objects.create_password_reset_code(user)
				password_reset_code.send_password_reset_email()
				return Response({ 'email' : email}, status=status.HTTP_201_CREATED)
		except User.DoesNotExist:
			pass
		return Response({ 'detail' : _('Password reset not allowed.')}, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetVerify(APIView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.CodeSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        code = serializer.data.get('code', '')

        try:
            password_reset_code = PasswordResetCode.objects.get(code=code)

            # Delete password reset code if older than expiry period
            delta = date.today() - password_reset_code.timestamp.date()
            if delta.days > PasswordResetCode.objects.get_expiry_period():
                password_reset_code.delete()
                raise PasswordResetCode.DoesNotExist()

            content = {'success': _('Email address verified.')}
            return Response(content, status=status.HTTP_200_OK)
        except PasswordResetCode.DoesNotExist:
        	pass
        content = {'detail': _('Unable to verify user.')}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetVerified(APIView):
	authentication_classes = ()
	permission_classes = (permissions.AllowAny,)
	serializer_class = serializers.PasswordResetVerifiedSerializer
	
	def post(self, request, format=None):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception = True)
		code = serializer.data.get('code')
		password = serializer.data.get('password')
		
		try:
			password_reset_code = PasswordResetCode.objects.get(code=code)
			password_reset_code.user.set_password(password)
			password_reset_code.user.save()
		
			# Delete password reset code just used
			password_reset_code.delete()
			
			content = {'success': _('Password reset.')}
			return Response(content, status=status.HTTP_200_OK)
		except PasswordResetCode.DoesNotExist:
			pass
		content = {'detail': _('Unable to verify user.')}
		return Response(content, status=status.HTTP_400_BAD_REQUEST)
		
        





class UserDetail(generics.RetrieveUpdateAPIView):
	serializer_class = serializers.UserSerializer
	permission_classes = (permissions.IsAuthenticated,)
	
	def retrieve(self, request, format=None):
		serializer = self.serializer_class(request.user)
		return Response(serializer.data)
	
	def update(self, request, format=None):
		serializer = self.serializer_class(request.user, data = request.data, partial = True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)
        
    