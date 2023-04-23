from django.contrib import admin

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.forms import PasswordInput

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


# Register your models here.


User = get_user_model()

class UserCreationForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email')
        

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class CustomUserAdmin(UserAdmin):
    #form = UserCreationForm
    list_display = ('username','email', 'first_name', 'last_name', 'is_staff')
    ordering = ("email",'username')

    fieldsets = (
    	(None, { 'fields' : ('username','password'), }),
    	(_('Personal Information'), 
    		{ 
    			'fields' : ('first_name','last_name','email') 
    		}
    	),
    	(_('Permissions'), 
    		{ 
    			'fields' : (
    				'is_superuser',
    				'is_staff',
    				'is_active',
    				'is_verified', 
    				'enable_notifications', 
    				'user_permissions',
    				'groups'
    			) 
    		}
    	),
    	(_('Important dates'), { 'fields' : ('birth_date','last_login')}),
    	(_('Image'), { 'fields' : ('avatar',)})
    )
    
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)