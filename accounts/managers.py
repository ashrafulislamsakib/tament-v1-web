import os
import binascii

from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

#from .models import SignupCode

# Create your model managers here.

EXPIRY_PERIOD = 5 # minutes

def _generate_code():
	return binascii.hexlify(os.urandom(3)).decode('utf-8')



class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with an email, username and password.
        """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
        
        
        
        

 
def send_multi_format_email(template_prefix, template_ctxt, target_email):
	subject_file = f'accounts/{template_prefix}_subject.txt'
	txt_file = f'accounts/{template_prefix}.txt'
	msg = EmailMultiAlternatives(
			render_to_string(subject_file, template_ctxt).strip(),  #subject
			render_to_string(txt_file, template_ctxt), # content 
			settings.EMAIL_HOST_USER, # from 
			[target_email] # to
		)
	msg.send()




        
        
        
class AbstractBaseCode(models.Model):
    """
    Abstract model for `SignupCode` `PasswordResetCode` `EmailChangeCode`
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(_('code'), max_length=6, primary_key=True,editable = False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.code
        
    
    def send_mail(self,prefix):
    	ctx = {
    		'email': self.user.email,
    		'first_name': self.user.first_name,
    		'username': self.user.username,
    		'code': self.code
    	}
    	send_multi_format_email(prefix, ctx, target_email=self.user.email)
    
 


class SignupCodeManager(models.Manager):
	def create_signup_code(self,user):
		code = _generate_code()
		signup_code = self.create(user=user, code=code)
		
		return signup_code
		
	def set_user_is_verified(self,code):
		try:
			obj = self.get_queryset().get(code=code)
			obj.user.is_verified = True
			obj.user.save()
			return True	
		except:
			pass
		return False
		


class PasswordResetCodeManager(models.Manager):
    def create_password_reset_code(self, user):
        code = _generate_code()
        password_reset_code = self.create(user=user, code=code)

        return password_reset_code

    
    def get_expiry_period(self):
        return EXPIRY_PERIOD


class EmailChangeCodeManager(models.Manager):
    def create_email_change_code(self, user, email):
        code = _generate_code()
        email_change_code = self.create(user=user, code=code, email=email)

        return email_change_code

    def get_expiry_period(self):
        return EXPIRY_PERIOD
		
		
		
		

		