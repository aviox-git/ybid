#imports
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from user.models import  AccountInfo , UserAddress , CardsInfo , ForgetPassword
from random import *
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.db.models import Q
from login.context_processors import getDomain
from login.helper_fun import StaffUserOnly
from datetime import date
from core.context_processors import getPublic_Config
from django.contrib.sites.shortcuts import get_current_site
import urllib
import json


def todaydate(request):
	today = date.today()
	return today

def mailSend(subject, recipient_list, message="", html_message=""):
	try:
		email_from = settings.EMAIL_HOST_USER
		send_mail( subject, message, email_from, recipient_list, html_message=html_message )
		return True
	except Exception as e:
		print(str(e))
		return False

class AdminLogin(View):
	template_name = 'admin-login.html'
	
	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,{})

	def post(self,request,*args, **kwargs):
		admin_email = request.POST.get("email")
		admin_password = request.POST.get("password")
		remeber_password = request.POST.get("rember_me")
		try:
			if admin_email !="" and admin_password !="":
				user = User.objects.get(Q(email=admin_email) | Q(username=admin_email))
				if user.is_staff == True or user.is_superuser == True:
					userauth = authenticate(username=user.username, password=admin_password)
					if userauth:
							login(request, user,backend='django.contrib.auth.backends.ModelBackend')
							return HttpResponseRedirect('/login/admin_home')
					else:
						messages.error(request,'Incorrect password given.')
						return HttpResponseRedirect('/login/admin-login')
				else:
					messages.error(request,'You don\'t Have Permission To Access this,Please Login With Right Credentials')
					return HttpResponseRedirect('/login/admin-login')

			else:
				messages.error(request,'Please Enter Email and Password')
				return HttpResponseRedirect('/login/admin-login')

		except Exception as e:
			print(e)
			messages.error(request,'Incorrect email or username  given.')
			return HttpResponseRedirect('/login/admin-login')


class AdminLogout(StaffUserOnly, View):
	def get(self,request,*args, **kwargs):
		logout(request)
		return HttpResponseRedirect('/login/admin-login')



class LoginView(View):
	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		password = request.POST.get('password')
		next_ = request.POST.get('next_')

		try:
			if email != "" and password != "": 
				user= User.objects.get(email = email)
				
				if user.is_active == True:
					userauth = authenticate(username=user.username, password=password)
					if userauth:
						login(request, user,backend='django.contrib.auth.backends.ModelBackend')
						if next_ != 'None':
							return HttpResponseRedirect(next_)
						return HttpResponseRedirect('/')
					else:
						messages.error(request,'Invalid credentials.')
						return HttpResponseRedirect('/login/')
				else:
					link = 'email_verification/'+str(user.pk)
					messages.success(request,"Your account has not been verified. Please <a href='"+link+"' class='ver_link'>click here </a>to resend verification email.")
					return HttpResponseRedirect('/login/')
			else:
				messages.info(request,'Invalid Email and Password.')
				return HttpResponseRedirect('/login/')

		except Exception as e:
			print(str(e))
			messages.info(request,'No such account exist.')
			return HttpResponseRedirect('/login/')
		

class ForgetPass(View):
	template_name = 'public_forget_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})

	def post(self, request, *args, **kwargs):
		email = request.POST.get('forget_email')
	
		try:
			user = User.objects.get(email=email)
			code = randint(100000, 999999) 
			fg_pwd = ForgetPassword(user_id=user.id,code=code)
			fg_pwd.save()
			data =  getDomain(request)
			site_name = (data['site_name'])
			date = todaydate(request)
			current_site =  request.build_absolute_uri('/')
			
			public =  getPublic_Config(request)
			public_logo = (public['public_logo'])
			static_url = settings.STATIC_URL
			link = str(current_site)+"login/reset_password/"+str(code)
			content_html = render_to_string("forget_password.html", locals())
			recipients = [email]
			email_from = settings.EMAIL_HOST_USER
			subject = "Reset Password"
			send_status = mailSend(subject, recipients, html_message=content_html)
			
			if send_status:
				messages.success(request,'Please check your email now to reset password.')
			else:
				messages.error(request,'Some error occur. Retry or contact with administrator.')
		
		except User.DoesNotExist:
		 	messages.error(request,'This email address is not registred.')
	
		except Exception as e:
		 	raise e
		 	messages.error(request,'Some error occur. Retry or contact with administrator.')
		return HttpResponseRedirect('forget_password')


class ResetPassword(View):
	template_name = 'public_new_password.html'

	def get(self, request, *args, **kwargs):
		code=kwargs.get('code')
		return render(request,self.template_name,locals())

	def post(self, request, *args, **kwargs):
		password = request.POST.get("password")
		c_password = request.POST.get("conf_password")
		code = kwargs.get('code')
		if len(password) > 0 and password == c_password:
			try:
				u = ForgetPassword.objects.get(code=code)
				u.user.set_password(password)
				u.user.save()
				messages.success(request,'Password changed successfully.')
				return HttpResponseRedirect('/login/')
			except  ForgetPassword.DoesNotExist:
				messages.error(request,'Some error occur please try again later.')
				return HttpResponseRedirect('/login/reset_password/'+ str(code))
		else:
			messages.error(request,'Password Does Not Match.')
			return HttpResponseRedirect('/login/reset_password/'+ str(code))



class LogoutView(LoginRequiredMixin, View):
	login_url = '/login/'
	
	def get(self,request,*args, **kwargs):
		logout(request)
		return HttpResponseRedirect('/')