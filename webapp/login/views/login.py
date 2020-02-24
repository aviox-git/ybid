from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import View

# Create your views here.

class LoginView(View):
	def post(self, request, *args, **kwargs):
		print("----------login", request.POST)
		email = request.POST.get('email')
		password = request.POST.get('password')
		next_ = request.POST.get('next_')
		return HttpResponseRedirect('forget_password')


class ForgetPass(View):
	template_name = 'public_forget_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})

class ResetPassword(View):
	template_name = 'public_new_password.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})
