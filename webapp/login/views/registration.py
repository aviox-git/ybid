from django.shortcuts import render
from django.views.generic import View


class Registration(View):
	template_name = 'public_login.html'

	def get(self, request, *args, **kwargs):	
		return render(request,self.template_name,locals())
