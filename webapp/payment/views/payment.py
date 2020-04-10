from django.shortcuts import render,HttpResponseRedirect, redirect,HttpResponse
from django.urls import reverse
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.models import User
from django.conf import settings
import stripe
import json
from user.models import  AccountInfo , UserAddress
from django.contrib import messages


stripe.api_key = settings.STRIPE_SECRET_KEY




class PaymentFailed(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = 'public_payment_failed.html'
	def get(self,request):
		return render(request,self.template_name,locals())

class PaymentSuccessfull(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = 'public_payment_successful.html'
	
	def get(self, request):
		return render(request,self.template_name,locals())


class StripeCallBackUrl(LoginRequiredMixin, View):
	def get(self, request):
		auth_code = request.GET.get('code')
		
		try:
			response = stripe.OAuth.token(
			  grant_type = 'authorization_code',
			  code = auth_code,
			)
			# Access the connected account id in the response
			connected_account_id = response.get('stripe_user_id')
			print(connected_account_id)
			user_stripe = AccountInfo.objects.filter(user = request.user).update(strip_number = connected_account_id)
			messages.success(request,"Stripe account successfully connect.")
			return HttpResponseRedirect('/users/')
		
		except Exception as e:
			messages.error(request, str(e.error.error_description))
			return HttpResponseRedirect('/users/')