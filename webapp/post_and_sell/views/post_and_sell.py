from django.shortcuts import render
from django.views.generic import View



class PostView(View):
	template_name = 'public_post_and_sell.html'

	def get(self, request, *args, **kwargs):
		active_dashboard = "active_dash"
		active_post = "active_post"
		return render(request,self.template_name,locals())


class ManagePosting(View):
	template_name = 'public_manage_posting.html'

	def get(self, request, *args, **kwargs):
		active_dashboard = "active_dash"
		active_manage_posting = "active_manage_posting"
		return render(request,self.template_name,locals())



class SalesOrder(View):
	template_name = 'public_sales_order.html'

	def get(self, request, *args, **kwargs):
		active_dashboard = "active_dash"
		active_sales = "active_sales"
		return render(request,self.template_name,locals())


class OrderHistory(View):
	template_name = 'public_order_history.html'

	def get(self, request, *args, **kwargs):
		active_dashboard = "active_dash"
		active_history = "active_history"
		return render(request,self.template_name,locals())