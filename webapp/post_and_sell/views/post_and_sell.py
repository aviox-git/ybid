from django.shortcuts import render
from django.views.generic import View



class PostAndSell(View):
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



class PublicSalesOrder(View):
	template_name = 'public_sales_order.html'

	def get(self, request, *args, **kwargs):
		active_dashboard = "active_dash"
		active_sales = "active_sales"
		return render(request,self.template_name,locals())


class PublicOrderHistory(View):
	template_name = 'public_order_history.html'

	def get(self, request, *args, **kwargs):
		active_dashboard = "active_dash"
		active_history = "active_history"
		return render(request,self.template_name,locals())

class AdminManagePostings(View):
	template_name = 'admin-manage-posting.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,locals())


		