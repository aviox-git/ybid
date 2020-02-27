from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from login.helper_fun import StaffUserOnly
from simplepages.models import Page
import json
# Create your views here.


class Homepage(TemplateView):
	template_name = 'public_home_page.html'
	def get(self, request):
		return render(request,self.template_name,locals())




class Pages(PermissionRequiredMixin, StaffUserOnly, TemplateView):
	permission_required = 'simplepages.view_page'
	template_name = '9011-TICKETS-MANAGE-CONTENT.html'
	def get(self, request, *args, **kwargs):
		pages=Page.objects.filter(delete_status=False).order_by('-id')
		return render(request,self.template_name,locals())
		
class AddPage(PermissionRequiredMixin, StaffUserOnly, TemplateView):
	permission_required = 'simplepages.view_page'
	template_name = '9012-TICKETS-ADD-PAGES.html'
	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		title=request.POST.get('page_title')
		content=request.POST.get('page_content')
		url=request.POST.get('page_url')
		background_image=request.FILES.get('background_image')
		page_obj=Page(
			title=title,
			content=content,
			url=url,
			background_image=background_image
			)
		page_obj.save()
		return redirect('pages')


# Change single page status	
class PageStatus(PermissionRequiredMixin, StaffUserOnly, View):
	permission_required = 'simplepages.view_page'
	def get(self,request):
		page_id = request.GET.get('page_id')
		response={}
		try:
			page_obj=Page.objects.get(id=int(page_id))
			if page_obj.status:
				page_obj.status=False
			elif page_obj.status==False:
				page_obj.status=True
			page_obj.save()
			response['status']=True
		except Exception as e:
			raise e
			response['status']=False
		return HttpResponse(json.dumps(response), content_type="application/json")
# Delete single page 	
class DeletePage(PermissionRequiredMixin, StaffUserOnly, View):
	permission_required = 'simplepages.view_page'
	def get(self,request):
		page_id = request.GET.get('page_id')
		response={}
		try:
			page=Page.objects.get(id=int(page_id))
			page.delete_status=True
			page.save()
			response['status']=True
		except Exception as e:
			raise e
			response['status']=False
		return HttpResponse(json.dumps(response), content_type="application/json")

# edit page
class EditPage(PermissionRequiredMixin, StaffUserOnly, TemplateView):
	permission_required = 'simplepages.view_page'
	template_name = '9013-TICKETS-EDIT-PAGE.html'
	def get(self, request, *args, **kwargs):
		page_id=kwargs.get('page_id')
		try:
			page=Page.objects.get(id=int(page_id))
		except Exception as e:
			raise e
		return render(request,self.template_name,locals())
	def post(self, request, *args, **kwargs):
		page_id=kwargs.get('page_id')
		title=request.POST.get("edit_title")
		content=request.POST.get("edit_content")
		url=request.POST.get("edit_url")
		background_image=request.FILES.get('background_image')
		try:
			page_obj=Page.objects.get(id=int(page_id))
			page_obj.title=title
			page_obj.content=content
			page_obj.url=url
			if background_image:
				page_obj.background_image=background_image
			page_obj.save()
		except Exception as e:
			raise e
		return HttpResponseRedirect("/pages")

# Change selected page status	
class SelectedPagesStatus(PermissionRequiredMixin, StaffUserOnly, View):
	permission_required = 'simplepages.view_page'
	def post(self,request):
		selected = request.POST.getlist('selected_pages[]')
		status=request.POST.get('status')
		response={}
		try:
			if status=='true':
				Page.objects.filter(id__in=selected).update(status=True)
			else:
				Page.objects.filter(id__in=selected).update(status=False)
			response['status']=True
		except Exception as e:
			raise e
			response['status']=False
		return HttpResponse(json.dumps(response), content_type="application/json")

# get created pages view
class GetPages(View):
	template_name='dynamic_page.html'
	def get(self, request, *args, **kwargs):
		try:
			url=kwargs.get('page')
			page_html=Page.objects.get(url=url)
		except Exception as e:
			return HttpResponse("404 page not found")
		return render(request,self.template_name,locals())
