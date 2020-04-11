#imports
from django.views.generic import View
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from user.models import AccountInfo , UserAddress , CardsInfo , ForgetPassword
from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from user.tokens import account_activation_token
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from core.models import Config
from login.context_processors import getDomain
from datetime import date
import json
from core.context_processors import getPublic_Config
import urllib
from django.core.exceptions import ObjectDoesNotExist

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

class PublicRegistration(View):
	template_name = 'public_login_registration.html'

	def get(self, request, *args, **kwargs):
		next_ = request.GET.get('next')	
		if request.user.is_authenticated:
			return HttpResponseRedirect("/")

		return render(request,self.template_name,locals())

	def post(self, request, *args, **kwargs):
		first_name=request.POST.get("first_name")
		last_name=request.POST.get("last_name")
		email=request.POST.get("email").lower()
		remail=request.POST.get("remail").lower()
		password=request.POST.get("password")
		c_password = request.POST.get("confirm_password")
		country=request.POST.get("parent_country")
		state=request.POST.get("state")
		terms = request.POST.get("terms")
		request.session.modified = True


		try:
			user = User.objects.filter(email=email).count()
			if user > 0:
					messages.info(request,"User already exist.")
					return HttpResponseRedirect('/login/')
			else:
				raise User.DoesNotExist
		
		except User.DoesNotExist:
			if len(password) > 0 and len(email) > 0 and password == c_password and email == remail:
				user = User.objects.create_user(
						username=email,
						email=email,
						password=password
						)
				user.first_name = first_name
				user.last_name = last_name
				user.is_active = False
				user.save()
				profile, created = AccountInfo.objects.get_or_create(
					user = user,
					terms_condition = terms
					)
				# profile.save()
				address, create = UserAddress.objects.get_or_create(
					info = profile,
					)
				address.country = country
				address.state = state
				address.save()

				data =  getDomain(request)
				site_name = (data['site_name'])
				date = todaydate(request)
				current_site =  request.build_absolute_uri('/')[:-1]
				public =  getPublic_Config(request)
				public_logo = (public['public_logo'])

				content_html = render_to_string('email_registration_verification.html', {
		                'user': user,
		                'domain': current_site,
		                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
		                'token':account_activation_token.make_token(user),
		                'site_name':site_name,
		                'date':date,
		                'public_logo':public_logo
		            })
				
				recipients = [email]
				email_from = settings.EMAIL_HOST_USER
				subject = "Email verification"
				send_status = mailSend(subject, recipients, html_message = content_html)
				link = 'email_verification/'+str(user.pk)

				if send_status:
					logout(request)
					messages.success(request,'Please check your email account for verification email.')
					return HttpResponseRedirect('/login/')
					
				else:
					messages.error(request,"Your account has not been verified. Please <a  href='"+link+"'  class='ver_link'>click here </a>to resend verification email.")
					return HttpResponseRedirect('/login/')
					
			else:
				messages.error(request,"Password or email does not match.")
				return HttpResponseRedirect('/login/')

class EmailVerification(View):
	template_name = 'public_login.html'
	
	def get(self, request, user_id):
		user = User.objects.get(pk=user_id)
		data =  getDomain(request)
		site_name = (data['site_name'])
		date = todaydate(request)
		static_url = settings.STATIC_URL
		current_site =  request.build_absolute_uri('/')[:-1]

		public =  getPublic_Config(request)
		public_logo = (public['public_logo'])
		
		content_html = render_to_string('email_registration_verification.html', {
                'user': user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'site_name':site_name,
                'date':date,
                'static_url':static_url,
                'public_logo':public_logo
            })
		
		recipients = [user.email]
		email_from = settings.EMAIL_HOST_USER
		subject = "Email verification"
		send_status = mailSend(subject, recipients, html_message=content_html)
		if send_status:
			messages.success(request,'Please check your email account for verification email.')
			return HttpResponseRedirect('/login/')
		else:
			messages.error(request,'Some error occur. Retry or contact with administrator.')
			return HttpResponseRedirect('/login/')

		

class CheckEmail(View):
	def post(self, request, *args, **kwargs):
		response = {}
		email = request.POST.get('email').lower()
		user_email = User.objects.filter(email = email).count()

		if user_email > 0:
			response['message'] = "Email already exist"
			response['status'] = True		
		else:
			response['status'] = False
		return HttpResponse(json.dumps(response), content_type = 'application/json')