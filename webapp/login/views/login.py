from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from user.models import  AccountInfo , UserAddress
from datetime import date
# Create your views here.

class LoginView(View):
	def post(self, request, *args, **kwargs):
		print("----------login", request.POST)
		email = request.POST.get('email')
		password = request.POST.get('password')
		next_ = request.POST.get('next_')

		try:
			if email != "" and password != "": 
				user= User.objects.get(email = email)
				
				if user.is_active == True:
					userauth = authenticate(username=user.username, password=password)
					if userauth:
						print("-----------------",userauth)
						login(request, user,backend='django.contrib.auth.backends.ModelBackend')
						print("8888888888",next_)
						if next_ != 'None':
							return HttpResponseRedirect(next_)
						return HttpResponseRedirect('/')
					else:
						messages.info(request,'Invalid password.')
						return HttpResponseRedirect('/login/')
				else:
					link = 'email_verification/'+str(user.pk)
					messages.success(request,"Your account has not been verified. Please <a href='"+link+"'>click here </a>to resend verification email.")
					return HttpResponseRedirect('/login/')
			else:
				messages.info(request,'Please Enter Email and Password.')
				return HttpResponseRedirect('/login/')

		except Exception as e:
			print(str(e))
			messages.info(request,'No such account exist.')
			return HttpResponseRedirect('/login/')
		


class ForgetPass(View):
	template_name = 'public_forget_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})

class ResetPassword(View):
	template_name = 'public_new_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})
