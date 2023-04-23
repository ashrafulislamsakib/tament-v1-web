from django.conf import settings

from django.contrib.auth import get_user_model
from django.contrib.auth import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import SignupCode

@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
	print('log in =========')


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    print('log out =========')
    
    
 
@receiver(post_save, sender = get_user_model())
def user_save_receiver(sender,instance,created,*args,**kwargs):
	if created:
		must_verify = getattr(settings,'VERIFY_BY_EMAIL',False)
		verified = must_verify == False
		instance.is_verified = verified
		instance.save()
		signup_code = SignupCode.objects.create_signup_code(instance)
		if must_verify:
			signup_code.send_signup_email()


