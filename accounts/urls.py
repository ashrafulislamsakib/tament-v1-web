from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = DefaultRouter()

api_urlpatterns = [
	path('me', views.UserDetail.as_view()),
	path('signup', views.SignupAPIView.as_view()),
	path('login', views.LoginAPIView.as_view()),
	path('logout', views.Logout.as_view()),
	
	
	path('verify-signup', views.SignupVerifyAPIView.as_view()),
	path('password-change', views.PasswordChangeAPIView.as_view()),
	path('password-reset', views.PasswordResetAPIView.as_view()),
	path('password-reset/verify', views.PasswordResetVerify.as_view()),
	path('password-reset/done', views.PasswordResetVerified.as_view()),
	#path('api/', include(router.urls)),
]


urlpatterns = [
	path('api/accounts/', include(api_urlpatterns)),
	
]

urlpatterns = format_suffix_patterns(urlpatterns)