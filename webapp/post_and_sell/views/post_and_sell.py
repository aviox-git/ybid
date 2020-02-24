from django.shortcuts import render
from django.views.generic import View



class PostView(View):
	template_name = 'public_post_and_sell.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})


class ManagePosting(View):
	template_name = 'public_manage_posting.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})



class SalesOrder(View):
	template_name = 'public_sales_order.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})


class OrderHistory(View):
	template_name = 'public_order_history.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})