from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()






class SignupSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username','email','password','first_name','last_name')
		
	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		user.save()
		return user
		
		


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(required = True,max_length = 255)
	password = serializers.CharField(required = True,max_length = 128)




class CodeSerializer(serializers.Serializer):
	code = serializers.CharField(max_length = 6,required = True)



class PasswordChangeSerializer(serializers.Serializer):
	password = serializers.CharField(required = True,max_length = 128)
	


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
 
 
 
class PasswordResetVerifiedSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=128)
 


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'first_name',
			'last_name',
			'username',
			'email',
			'enable_notifications',
			'birth_date',
			'avatar'
		)
	
	