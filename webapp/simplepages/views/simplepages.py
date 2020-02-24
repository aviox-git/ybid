from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.views.generic import View,TemplateView
# Create your views here.


class Homepage(TemplateView):
	template_name = 'public_home_page.html'
	def get(self, request):
		return render(request,self.template_name,locals())

