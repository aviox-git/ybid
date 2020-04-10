from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from random import *
from django.conf import settings
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from simplepages.models import FAQCategory, FAQ
from login.helper_fun import StaffUserOnly
from django.contrib.auth.mixins import PermissionRequiredMixin

class PublicFAQWeb(View):
	login_url = '/login/'
	template_name = 'public_faq.html'
	def get(self, request, *args, **kwargs):
		active_faq = "active"
		category = FAQCategory.objects.filter(status = True).order_by('-sort_order')
		return render(request,self.template_name,locals())


# Create your views here.
class FAQCategoryView(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "simplepages.view_faqcategory"
	template_name = 'admin_faq-category.html'

	def get(self,request):
		categories = FAQCategory.objects.all()
		return render(request,self.template_name,locals())
	# Delete the FAQ category
	def post(self,request):
		cat_id = request.POST.get('cat_id')
		FAQCategory.objects.get(pk = cat_id).delete()
		messages.success(request,'Successfully deleted')
		response = {}
		return HttpResponse(json.dumps(response), content_type="application/json")


class AddFAQCategoryView(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "simplepages.view_faqcategory"

	def get(self,request):
		return render(request,'admin_faq-category-add.html',locals())

	def post(self,request):
		status =  request.POST.get('status')
		order =  request.POST.get('order')
		category =  request.POST.get('category')

		if status and category and order:
			cat = FAQCategory(category_name = category,sort_order = order)
			if status == 'active':
				cat.status = True
			cat.save()
			messages.success(request,'FAQ Category Successfully Added')
		else:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/faq-category')


class EditFAQCategoryView(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "simplepages.view_faqcategory"
	def get(self,request, cat_id):
		cat = FAQCategory.objects.get(pk = cat_id)
		return render(request,'admin_faq-category-edit.html',locals())

	def post(self,request,cat_id):
		cat_id = cat_id
		status =  request.POST.get('status')
		order =  request.POST.get('order')
		name =  request.POST.get('category')
		try:
			if cat_id:
				category = FAQCategory.objects.get(pk = cat_id)
				if name:
					category.category_name = name
				if order:
					category.sort_order = order
				if status == 'active':
					category.status = True
				else:
					category.status = False
				category.save()
				messages.success(request,'FAQ Category Successfully Added')
			else:
				messages.error(request,'Something Went Wrong')
		except Exception as e:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/faq-category')

class FAQView(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "simplepages.view_faq"
	template_name = 'admin_faq.html'

	def get(self,request):
		faqs = FAQ.objects.all()
		return render(request,self.template_name,locals())

	# Delete the FAQ 
	def post(self,request):
		faq_id = request.POST.get('faq_id')
		FAQ.objects.get(pk = faq_id).delete()
		response = {}
		return HttpResponse(json.dumps(response), content_type="application/json")


class AddFAQView(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "simplepages.view_faq"
	def get(self,request):
		category = FAQCategory.objects.all()
		return render(request,'admin_faq-add.html',locals())

	def post(self,request):
		category_id = request.POST.get('category')
		question = request.POST.get('question')
		order = request.POST.get('order')
		status = request.POST.get('status')
		answer = request.POST.get('answer')

		if category_id and question and answer:
			faq = FAQ(category_id = category_id, question = question, answer = answer)
			if status == 'active':
				faq.status = True
			if order:
				faq.sort_order = order
			faq.save()
		messages.success(request,'Successfully Faq Added.')
		return HttpResponseRedirect('/faq')


class EditFAQView(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "simplepages.view_faq"
	def get(self,request, faq_id):
		category = FAQCategory.objects.all()
		faq = FAQ.objects.get(pk = faq_id)
		return render(request,'admin_faq-edit.html',locals())

	def post(self,request,faq_id):
		faq_id = faq_id
		category_id = request.POST.get('category')
		question = request.POST.get('question')
		order = request.POST.get('order')
		status = request.POST.get('status')
		answer = request.POST.get('answer')
		try:
			if faq_id:
				faq = FAQ.objects.get(pk = faq_id)
				if category_id:
					category = FAQCategory.objects.get(pk = category_id)
					faq.category = category
				if order:
					faq.sort_order = order
				if status == 'active':
					faq.status = True
				else:
					faq.status = False
				if answer:
					faq.answer = answer
				if question:
					faq.question = question
				faq.save()
				messages.success(request,'FAQ Category Successfully Added')
			else:
				messages.error(request,'Something Went Wrong')
		except Exception as e:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/faq')