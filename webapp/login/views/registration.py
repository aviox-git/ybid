from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from user.models import AccountInfo , UserAddress
from django.core.mail import send_mail
from core.models import Config
from login.context_processors import getDomain
from django.conf import settings
from django.contrib import messages


class Registration(View):
	template_name = 'public_login.html'

	def get(self, request, *args, **kwargs):	
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

		try:
			user=User.objects.get(email=email)
			messages.info(request,"User already Exist.")
			return HttpResponseRedirect('/login/')
		except User.DoesNotExist:
			if password == c_password and email == remail:
				user=User.objects.create_user(
					username=email,
					email=email,
					password=password
					)
				user.first_name = first_name
				user.last_name = last_name
				user.is_active = False
				user.save()
				profile=AccountInfo(
					user=user,
					terms_condition=terms
					)
				profile.save()
				address = UserAddress(
					info=profile,
					country=country,
					state=state,)
				address.save()
				data =  getDomain(request)
				site_name = (data['site_name'])
				date = todaydate(request)
				current_site =  request.build_absolute_uri('/')[:-1]
				public =  getPublic_Config(request)
				public_logo = (public['public_logo'])

				content_html = render_to_string('email_verification.html', {
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
				send_status = mailSend(subject, recipients, html_message=content_html)
				link = 'email_verification/'+str(user.pk)

				if send_status:
					logout(request)
					messages.success(request,'Your request has been received. Please look for an email from ' + str(site_name) + ' for more details!. Thank you.')
					return HttpResponseRedirect('/login/')
					
				else:
					messages.error(request,"Your account has not been verified. Please <a  href='"+link+"'>click here </a>to resend verification email.")
					return HttpResponseRedirect('/login/')
					
			else:
				messages.error(request,"Password or Email Does Not Match.")
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
		
		content_html = render_to_string('email_verification.html', {
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
			messages.success(request,'Your request has been received. Please look for an email from ' + str(site_name) + ' for more details!. Thank you.')
			return HttpResponseRedirect('/login/')
		else:
			messages.error(request,'Some error occur. Retry or contact with administrator.')
			return HttpResponseRedirect('/login/')
		

class CheckEmail(View):
	def post(self, request, *args, **kwargs):
		response = {}
		email = request.POST.get('email').lower()
		try:
			user_email = User.objects.get(email = email)
			response['message'] = "Email Already Exist"
			response['status'] = True
			
		except User.DoesNotExist:
			response['status'] = False
		return HttpResponse(json.dumps(response), content_type = 'application/json')
