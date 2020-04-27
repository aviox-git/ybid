from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from user.models import  AccountInfo , UserAddress , CardsInfo , ForgetPassword
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from random import *
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from user.tokens import account_activation_token
from core.models import Config
from login.context_processors import getDomain
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from email.mime.image import MIMEImage
from datetime import date, datetime
import json
from django.utils import timezone
from core.context_processors import getPublic_Config
from os.path import basename


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

class MyAccountInfo(View):
	template_name = 'public_my_account_info.html'

	def get(self,request,*args,**kwargs):
		active_dashboard = "active_dash"
		active_account = "active_account"
		profile = AccountInfo.objects.get(user=request.user)
		add = UserAddress.objects.get(info=request.user.accountinfo)
		domain_name =  getDomain(request)
		site_name = (domain_name['site_name'])
		try:
			cards = CardsInfo.objects.get(info=request.user.accountinfo)
		except CardsInfo.DoesNotExist:
			pass
		return render(request,self.template_name,locals())


	def post(self,request,*args,**kwargs):
		email = request.POST.get('email').lower()
		old_pass = request.POST.get('old_pass')
		new_pass = request.POST.get('pass')
		company_name = request.POST.get('company_name')
		website = request.POST.get('website')
		strip_number = request.POST.get('pay_email')
		phone = request.POST.get('phone')
		billing_add = request.POST.get('billing_add')
		address = request.POST.get('address')
		country = request.POST.get('country')
		state = request.POST.get('state')
		city = request.POST.get('city')
		zipcode = request.POST.get('zip')
		credit_card_number = request.POST.get('cc_number')
		expiration_month = request.POST.get('month')
		expiration_year = request.POST.get('year')
		company_logo = request.FILES.get('logo')
		license = request.FILES.get('license')
		about_seller = request.POST.get('about_seller')
		terms = request.POST.get('terms')

		try:
			user = User.objects.get(id=request.user.id)
			expiration_date = expiration_month + '/' + expiration_year
			account = AccountInfo.objects.get(user=request.user)
			account.company_name = company_name
			account.website = website
			account.strip_number = strip_number
			account.phone = phone
			account.zipcode = zipcode
			if company_logo:
				account.company_logo = company_logo
			if license:
				account.business_license = license
			account.about_seller = about_seller
			account.terms = terms
			account.save()
			addd = UserAddress.objects.get(info=request.user.accountinfo)
			addd.billing_address = billing_add
			addd.address = address
			addd.country = country
			addd.state = state
			addd.city = city
			addd.save()
			cards,created = CardsInfo.objects.get_or_create(info = request.user.accountinfo)
			cards.credit_card_number = credit_card_number
			cards.expiration_date = expiration_date
			cards.save()
			
			if new_pass or request.user.email != email:
				if new_pass:
					userauth = authenticate(username=user.username, password=old_pass)
					if userauth:
						user.set_password(new_pass)
						user.save()
						messages.info(request,'Password Successfully Update ')
						logout(request)
						return HttpResponseRedirect('/')
					else:
						messages.error(request,'Incorrect old password')
						return HttpResponseRedirect('/users/')
				else:
					try:
						user = User.objects.get(email=email)
						messages.info(request,"User already Exist.")
						return HttpResponseRedirect("/users/")
						
					except User.DoesNotExist:
						user.username = user.email = email
						user.is_active = False
						user.save()
						link = 'email_verification/'+str(user.pk)
						
						messages.error(request,"Your account has not been verified. Please <a  href='"+link+"' class='ver_link'>click here </a>to resend verification email.")
						return HttpResponseRedirect('/login/')

		except Exception as e:
			print(e)
			messages.info(request,"Somting Wrong " + str(e))
		return HttpResponseRedirect('/users/')


class ConfirmEmail(View):
	def get(self,request,uidb64, token):
		try:
			uid = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
			data =  getDomain(request)
			site_name = (data['site_name'])
		except(TypeError, ValueError, OverflowError, User.DoesNotExist):
			user = None
		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			date = todaydate(request)
			current_site =  request.build_absolute_uri('/')
			public =  getPublic_Config(request)
			public_logo = (public['public_logo'])
			site_name = public['public_site_name']
			static_url = settings.STATIC_URL
			content_html = render_to_string('email_successfully_register.html',locals())
			recipients = [user.email]
			email_from = settings.EMAIL_HOST_USER
			subject = site_name.upper() + ' - SUCCESSFULLY-REGISTER'
			send_status = mailSend(subject, recipients, html_message=content_html)	
			login(request, user,backend='django.contrib.auth.backends.ModelBackend')
			return HttpResponseRedirect("/")
		else:
			messages.info(request,'Activation link is invalid!')
			return HttpResponseRedirect('/')



class PhotoUpload(View):
	template_name = 'public_photographer_upload.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})