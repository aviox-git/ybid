from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from login.helper_fun import StaffUserOnly
from simplepages.models import Page, ContactCategory, ContactUs, AdminReply, ContactAttachment, AdminReplyAttachment
from core.models import Company
import json
from django.contrib import messages
from core.context_processors import getPublic_Config
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage
from datetime import date
import random
from datetime import datetime, timedelta
from django.conf import settings
# Create your views here.

def todaydate(request):
	today = date.today()
	return today



def mailSend(subject, recipient_list,  message="", html_message="", attach = None):
	try:
		email_from = settings.EMAIL_HOST_USER
		mail = EmailMessage( subject, html_message, email_from, recipient_list )
		for attachment in attach:
			mail.attach_file(attachment)
		mail.content_subtype = "html" 
		mail.send()
		return True
	except Exception as e:
		print(str(e))
		return False


class Homepage(TemplateView):
	template_name = 'public_home_page.html'
	def get(self, request):
		active_home = "active"
		return render(request,self.template_name,locals())



def CreateTicekt(number):
	R = random.randint(3, 13)
	time =  datetime.now().strftime("%H%M")
	Time = int(time) * 3
	if number:
		inv = int(number[6:])
	else:
		inv = 12345
	INV = inv + R
	ticket = 'CT' + str(Time) + str(INV)
	return ticket


class PublicContact(TemplateView):
	template_name = 'public_contactus.html'
	def get(self, request, *args, **kwargs):
		active_contact = "active"
		contact_cats = ContactCategory.objects.filter(status = True)
		ticket = request.GET.get('ticket')
		if ticket:
			try:
				ticket = ContactUs.objects.get(inquiry = ticket)
			except ContactUs.DoesNotExist:
				messages.error(request, 'Invalid ticket number')
				return HttpResponseRedirect('/')

		return render(request,self.template_name,locals())


	def post(self, request):
		first_name = request.POST.get('f_name')
		last_name = request.POST.get('l_name')
		email = request.POST.get('email')
		msg = request.POST.get('msg')
		img = request.FILES.getlist('img')
		subject = request.POST.get('subject')
		inquiry_type = request.POST.get('inquiry_type')
		date_now = datetime.now()
		ticket = request.POST.get('ticket')
		deletedIndex = json.loads(request.POST.get('deletedIndexes'))

		if deletedIndex:
			for image in img:
				if image.name in  deletedIndex:
					img.remove(image)

		attach = []
		public =  getPublic_Config(request)
		site_name = (public['public_site_name'])

		if ticket:
			contactObj = ContactUs.objects.get(inquiry = ticket)
			admin_reply = AdminReply(contact = contactObj, message = msg)
			admin_reply.save()
			if img:
				for image in img:
					reply_attchment = AdminReplyAttachment.objects.create(reply = admin_reply, attachment = image)
					attach.append(settings.BASE_DIR +  reply_attchment.attachment.url)
		else:
			try:
				contact_num = ContactUs.objects.latest('pk')
				contact_num = contact_num.inquiry
			except ContactUs.DoesNotExist:
				contact_num = None

			ticket_num = CreateTicekt(contact_num)
			try:
				contact_cate = ContactCategory.objects.get(pk = inquiry_type)
				subject = site_name + ' - Contact - ' + contact_cate.category_name
				contactObj = ContactUs.objects.create(inquiry = ticket_num, category = contact_cate, first_name = first_name, last_name = last_name, email = email, subject = subject, message = msg)
				if img:
					for image in img:
						contact_attchment = ContactAttachment.objects.create(contact = contactObj, attachment = image)
						attach.append(settings.BASE_DIR +  contact_attchment.attachment.url)
			except Exception as e:
				print(e)
				messages.error(request,'Something went wrong.')
				return HttpResponseRedirect("/contact_us")
		try:
			company = Company.objects.latest('pk')
		except Company.DoesNotExist:
			company = None

		
		ticket_num = contactObj.inquiry
		first_name = contactObj.first_name
		last_name = contactObj.last_name
		email = contactObj.email
		
		date = todaydate(request)
		current_site =  request.build_absolute_uri('/')
		public =  getPublic_Config(request)
		public_logo = (public['public_logo'])
		static_url = settings.STATIC_URL
		content_html = render_to_string("emai-contact-mail.html", locals())
		recipients = [email]
		if company != None:
			recipients.append(company.email)
		email_from = settings.EMAIL_HOST_USER
		subject = contactObj.subject
		send_status = mailSend(subject, recipients, html_message=content_html, attach = attach)
		messages.success(request,'Request is sent successfully.')
		return HttpResponseRedirect("/contact_us")


class ContactCategoryAdd(StaffUserOnly, View):
	def get(self,request):
		return render(request,'admin_add_contact_category.html',locals())

	def post(self,request):
		status =  request.POST.get('status')
		category =  request.POST.get('category')

		if status and category:
			cat = ContactCategory(category_name = category)
			if status == 'active':
				cat.status = True
			cat.save()
			messages.success(request,'Contact category successfully added')
		else:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/contact-category')


class ContactCategoriesEditView(StaffUserOnly,View):
	def get(self, request,cat_id):
		cat = ContactCategory.objects.get(pk = cat_id)
		return render(request,'admin_contact_category_edit.html',locals())

	def post(self,request,cat_id):
		cat_id = cat_id
		status =  request.POST.get('status')
		name =  request.POST.get('category')
		try:
			if cat_id:
				category = ContactCategory.objects.get(pk = cat_id)
				if name:
					category.category_name = name
				if status == 'active':
					category.status = True
				else:
					category.status = False
				category.save()
				messages.success(request,'Conatct category uccessfully update')
			else:
				messages.error(request,'Something Went Wrong')
		except Exception as e:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/contact-category')




class ContactCategoriesView(StaffUserOnly,View):
	def get(self,request):
		contact_cats = ContactCategory.objects.all()
		return render(request,'admin_contact_category_list.html',locals())

	def post(self,request):
		cat_id = request.POST.get('cat_id')
		ContactCategory.objects.get(pk = cat_id).delete()
		response = {}
		return HttpResponse(json.dumps(response), content_type="application/json")



class AdminContactList(StaffUserOnly,View):
	def get(self,request):
		contacts = ContactUs.objects.all()
		return render(request,'admin-contact-list.html',locals())


	def post(self,request):
		con_id = request.POST.get('id')
		message = request.POST.get('message')
		attach = request.FILES.getlist('attach')
		contact = ContactUs.objects.get(pk = con_id)
		date_now = datetime.now()
		admin_reply = AdminReply(
			contact_id  = con_id,
			message = message,
			replied = True
			)
		admin_reply.save()
		img_list = []
		if attach:
			for image in attach:
				reply_attchment = AdminReplyAttachment.objects.create(reply = admin_reply, attachment = image)
				img_list.append(settings.BASE_DIR +  reply_attchment.attachment.url)

		try:
			company = Company.objects.latest('pk')
		except Company.DoesNotExist:
			company = None

		public =  getPublic_Config(request)
		site_name = (public['public_site_name'])

		date = todaydate(request)
		current_site =  request.build_absolute_uri('/')
		public =  getPublic_Config(request)
		public_logo = (public['public_logo'])
		static_url = settings.STATIC_URL
		content_html = render_to_string("email_admin-reply_email.html", locals())
		email = admin_reply.contact.email
		recipients = [email]

		if company != None:
			recipients.append(company.email)

		email_from = settings.EMAIL_HOST_USER
		subject =  contact.subject
		send_status = mailSend(subject, recipients, html_message=content_html, attach = img_list)
		messages.success(request,'Request is sent succesfully.')
		return HttpResponseRedirect('/public-contact-list')


class ManagePages(StaffUserOnly, TemplateView):
	template_name = 'admin_manage_pages.html'
	def get(self, request, *args, **kwargs):
		pages=Page.objects.filter(delete_status=False).order_by('-id')
		return render(request,self.template_name,locals())
		
class AddPage(StaffUserOnly, TemplateView):
	template_name = 'admin_add_pages.html'
	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,locals())

	def post(self,request,*args,**kwargs):
		title=request.POST.get('page_title')
		content=request.POST.get('page_content')
		url=request.POST.get('page_url')
		background_image=request.FILES.get('background_image')
		position = request.POST.get('position')
		page_obj=Page(
			title=title,
			content=content,
			url=url,
			background_image=background_image,
			postion  = position
			)
		page_obj.save()
		return redirect('pages')


# Change single page status	
class PageStatus(StaffUserOnly, View):
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
class DeletePage(StaffUserOnly, View):
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
class EditPage(StaffUserOnly, TemplateView):
	template_name = 'admin_edit_pages.html'
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
		position = request.POST.get('position')
		try:
			page_obj=Page.objects.get(id=int(page_id))
			page_obj.title=title
			page_obj.content=content
			page_obj.url=url
			page_obj.postion = position
			if background_image:
				page_obj.background_image=background_image
			page_obj.save()
		except Exception as e:
			raise e
		return HttpResponseRedirect("/pages")

# Change selected page status	
class SelectedPagesStatus(StaffUserOnly, View):
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
