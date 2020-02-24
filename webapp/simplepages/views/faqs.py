from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.views.generic import View,TemplateView



class FaqCategoryView(TemplateView):
	template_name = 'admin_faq_category.html'
	def get(self, request):
		return render(request,self.template_name,locals())


class AddFaqCategory(TemplateView):
	template_name = 'admin-add-faq-category.html'
	def get(self, request):
		return render(request,self.template_name,locals())