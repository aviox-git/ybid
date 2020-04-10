from django.shortcuts import render
from django.views.generic import View



class AdminProductView(View):
	template_name = 'admin-product-list.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,locals())