from django.shortcuts import render
from django.views.generic import View



class AdminPriceAndFee(View):
	template_name = 'admin-manage-price-and-fee.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,locals())