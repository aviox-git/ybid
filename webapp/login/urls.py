from django.urls import path
from .views import Registration, ForgetPass,ResetPassword,LoginView
urlpatterns = [
	# registration url 
	path('',Registration.as_view(), name='registration'),
	path('login',LoginView.as_view(), name='login'),


	path('forget_password',ForgetPass.as_view(), name='forget_password'),
	path('reset_password',ResetPassword.as_view(), name='reset_password'),
]