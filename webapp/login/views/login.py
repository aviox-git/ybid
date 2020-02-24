from django.shortcuts import render
from django.views.generic import View

# Create your views here.



class ForgetPass(View):
	template_name = 'public_forget_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})

class ResetPassword(View):
	template_name = 'public_new_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})
