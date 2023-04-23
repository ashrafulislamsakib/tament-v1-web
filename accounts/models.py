import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import (
	UserManager, 
	AbstractBaseCode, 
	SignupCodeManager,
	PasswordResetCodeManager,
	EmailChangeCodeManager
	
)

#UserManager, AbstractBaseCode, SignupCodeManager,PasswordResetCodeManager,EmailChangeCodeManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
	#id = models.UUIDField(primary_key = True, default = uuid.uuid4(), editable = False)
	username = models.CharField(_('username'),primary_key = True,db_index = True, max_length=255, unique=True)
	email = models.EmailField(_('email'), db_index=True, unique=True)
	enable_notifications = models.BooleanField(_('is notification enabled ?'),default = True)
	first_name = models.CharField(_('first_name'), max_length=255, null=True, blank = True)
	last_name = models.CharField(_('last_name'), max_length = 255, null=True, blank = True)
	is_active = models.BooleanField(_('is user active ?'), default=True)
	is_staff = models.BooleanField(_('is staff of site ?'), default=False)
	is_verified = models.BooleanField(_('is verified ?'), default=False)
	date_joined = models.DateTimeField(_('joined'), auto_now_add=True)
	birth_date = models.DateField(null = True, blank = True)
	avatar = models.FileField(_('user avatar'), null = True,blank = True ,upload_to ='accounts', default = 'accounts/user.png', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	
	objects = UserManager()
	
	def __str__(self):
		return self.username
	
	
	
	@property	
	def is_admin(self):
		return self.is_staff








class SignupCode(AbstractBaseCode):
	objects = SignupCodeManager()
	
	def send_signup_email(self):
		prefix = 'signup_email'
		self.send_mail(prefix)


class PasswordResetCode(AbstractBaseCode):
    objects = PasswordResetCodeManager()
    
    def send_password_reset_email(self):
    	prefix = 'password_reset_email'
    	self.send_mail(prefix)



class EmailChangeCode(AbstractBaseCode):
    email = models.EmailField(_('email address'), max_length=255)

    objects = EmailChangeCodeManager()



