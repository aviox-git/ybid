from django.shortcuts import render,HttpResponseRedirect, redirect,HttpResponse
from django.urls import reverse
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.models import User
from django.conf import settings
import stripe
import json
from user.models import  AccountInfo , UserAddress



stripe.api_key = settings.STRIPE_SECRET_KEY




class PaymentFailed(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = 'payment_failed.html'
	def get(self,request):
		return render(request,self.template_name,locals())

class PaymentSuccessfull(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = 'payment_successful.html'
	
	def get(self, request):
		return render(request,self.template_name,locals())


##################  stripe Account ####################
class StripeAccount(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = "stripe-account.html"
	def get(self,request):
		return render(request,self.template_name,locals())

	def post(self,request):
		response = {}
		stripe.api_key = settings.STRIPE_SECRET_KEY
		country = request.POST.get('for_country')
		address1 = request.POST.get('address_1')
		address2 = request.POST.get('address_2')
		city = request.POST.get('city') 
		state = request.POST.get('state')
		zipcode = request.POST.get('zip')
		emp_number = request.POST.get('emp_number')
		img = request.FILES.get('img')
		front_image = request.FILES.get('front_image')
		dob = request.POST.get('dob')
		ssn_number = request.POST.get('ssn_number')
		routing_number = request.POST.get('routing_number')
		account_number = request.POST.get('account_number')
		last_four = request.POST.get('last_four')

		try:
			back_img = stripe.File.create(
					    purpose="identity_document",
					    file=img
					  	)
			file_id = back_img['id']
			front_img = stripe.File.create(
					    purpose="identity_document",
					    file=front_image
					  	)
			front_file_id = front_img['id']
			account = stripe.Account.create(
					    country=country,
					    type='custom',
					    requested_capabilities=['card_payments', 'transfers'],
					    business_type = 'individual',
					    external_account = {
					      "object": "bank_account",
					      'country':country,
					      'currency':"USD",
					      'routing_number':routing_number,
					      'account_number':account_number,
					      "last4": last_four,

					    },
					    individual = {
						  'first_name':request.user.first_name,
						  'last_name':request.user.last_name,
						  'address':{
						  'city':city,
	  					  'country':country,
	  					  'line1': address1,
	  					  'postal_code': zipcode,
	  					  'state':state,
	  					  },
						  'email':request.user.email,
						  'phone': emp_number,
						  'ssn_last_4': ssn_number,
						  'verification': {
						  'document':{
						  'back': file_id,
						  'front':front_file_id
						   }

						  }
						  
						}
					)
			create_account_id = account['id']
			current_site =  request.build_absolute_uri('/')
			success_urls = str(current_site) + 'users/'
			failure_urls = str(current_site) + 'payment/stripe-account'
			account_links = stripe.AccountLink.create(
				  account= create_account_id ,
				  failure_url= failure_urls,
				  success_url = success_urls,
				  type='custom_account_verification',
				  collect='eventually_due',
				)
			acitvation_link = account_links['url']
			user_stripe = AccountInfo.objects.filter(user = request.user).update(strip_number = create_account_id)
			response['status'] = True
			response['url'] = acitvation_link
			return HttpResponse(json.dumps(response),content_type = 'application/json')
			
		except Exception as e:
			print(e.error.message)
			response['status'] = False
			response['message'] = str(e.error.message)
			return HttpResponse(json.dumps(response),content_type = 'application/json')