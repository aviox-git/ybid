#imports
from django.views.generic import View,TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.contrib.auth.models import Group, Permission 
from django.contrib.contenttypes.models import ContentType 
from django.apps import apps
from login.helper_fun import StaffUserOnly
from login.context_processors import getDomain
from django.contrib.sites.shortcuts import get_current_site
from datetime import date
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string, get_template
from core.context_processors import getPublic_Config
from django.contrib.auth.mixins import PermissionRequiredMixin


def todaydate(request):
	today = date.today()
	return today


class AdminSummary(StaffUserOnly,View):
	# permission_required = "auth.view_user"
	template_name = 'admin-summary.html'
	def get(self,request,*args, **kwargs):
		return render(request,self.template_name,locals())


class WebAppUsers(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "auth.view_user"
	template_name = 'admin_users.html'

	def get(self,request):
		users = User.objects.all().exclude(is_staff = True)
		invoice_list = []
		# for user in users:
		# 	try:
		# 		invoice = InvoiceOrder.objects.filter(user = user).latest('createdon')
		# 		invoice_list.append(invoice)

		# 	except InvoiceOrder.DoesNotExist:
		# 		pass
		
		return render(request,self.template_name,locals())

	def post(self,request):
		value = request.POST.get('value')
		value_list = request.POST.getlist('value_list[]')
		type_user = request.POST.get('type')
		
		if value:
			user = User.objects.get(pk = value)
			if user.is_active:
				user.is_active = False
			else:
				user.is_active = True
			user.save()
		elif value_list and type_user == 'deactive':
			user = User.objects.filter(pk__in = value_list).update(is_active = True)
		elif value_list and type_user == 'active':
			user = User.objects.filter(pk__in = value_list).update(is_active = False)
		return HttpResponse(json.dumps({}),content_type = 'application/json')


class EditWebAppUsers(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "auth.view_user"
	template_name = 'edit_users.html'
	def get(self,request,*args, **kwargs):
		user_id = kwargs.get('user_id')
		user = User.objects.get(id = user_id)
		return render(request,self.template_name,locals())

	def post(self,request,*args, **kwargs):
		user_id = kwargs.get('user_id')
		name = request.POST.get('name')
		status = request.POST.get('status')
		email = request.POST.get('email').lower()
		password = request.POST.get('password')
		repassword = request.POST.get('rpassword')

		try:
			user = User.objects.get(id=user_id)

			if password:
				if password == repassword:
					user.first_name = name
					user.email = email
					user.username = email
					if status=="A":
							user.is_active = True
					else:
						user.is_active = False
					user.set_password(password)
					user.save()
					return HttpResponseRedirect('/login/webapp-users')
				else:
					messages.error(request, 'Password does not match.')
					return HttpResponseRedirect('/login/edit-webapp-users/'+str(user_id))
			else:
				user.first_name = name
				user.email = email
				user.username = email
				if status=="A":
					user.is_active = True
				else:
					user.is_active = False
				user.save()
				return HttpResponseRedirect('/login/webapp-users')


		except Exception as e:
			print(str(e))
			return HttpResponseRedirect('/login/edit-webapp-users/'+str(user_id))


class AddWebAppUsers(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_user"
	template_name = 'admin_add_web_user.html'
	def get(self,request,*args, **kwargs):
		print(request.user)
		return render(request,self.template_name,{})


	def post(self,request,*args, **kwargs):
		name = request.POST.get('name')
		status = request.POST.get("status")
		password = request.POST.get("password")
		confirm_password = request.POST.get("confirm_password")
		email = request.POST.get('email')
		email = email.lower()
		try:
			User.objects.get(email=email)
			messages.error(request, 'User already exists with given email.')
			return HttpResponseRedirect('/login/add_web_user')

		except User.DoesNotExist:
			if password == confirm_password and password != "" and confirm_password !="":
				user = User.objects.create(
					email=email,
					username=email,
					first_name=name
					)
				if status=="A":
					user.is_active = True
				else:
					user.is_active = False
				user.set_password(password)
				user.save()
				messages.success(request, 'Staff entry done successfully.')
				return HttpResponseRedirect('/login/webapp-users')
			else:
				messages.error(request, 'Password does not match.')
				return HttpResponseRedirect('/login/add_web_user')



# super admin
class SuperAdmin(PermissionRequiredMixin, StaffUserOnly,TemplateView):
	permission_required = "auth.view_user"
	template_name = 'admin_super_admin.html'
	def get(self, request, *args, **kwargs):
		users = User.objects.filter(is_superuser=True).exclude(pk=request.user.id)
		return render(request,self.template_name,locals())

	def post(self,request):
		value = request.POST.get('value')
		if value:
			user = User.objects.get(pk = value)
			if user.is_active:
				user.is_active = False
			else:
				user.is_active = True
			user.save()
		return HttpResponse(json.dumps({}),content_type = 'application/json')


class EditAdmin(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_user"
	template_name = 'edit-admin.html'
	def get(self, request, *args, **kwargs):
		user_id = kwargs.get('user_id')
		user = User.objects.get(id=user_id)
		user_groups = user.groups.all()
		current_id = 0
		if user_groups:
			current_id = user_groups[0].id
		groups = Group.objects.all()
		model_items = ContentType.objects.exclude(app_label__in=["auth","contenttypes","sessions","social_django","admin"])
		selected_permissions = set(Permission.objects.filter(user=user_id).values_list('content_type__model',flat=True).distinct())
		model_list = map(lambda model_item: {"id":model_item.id,"name":model_item.name,"slug":(model_item.name).replace(" ","")}, model_items) 
		return render(request,self.template_name,locals())


	def post(self,request,*args, **kwargs):
		user_id = kwargs.get('user_id')
		name = request.POST.get('name')
		new_pass = request.POST.get('password')
		repassword = request.POST.get('repassword')   
		role = request.POST.get('role')
		status = request.POST.get('status')
		email = request.POST.get('email')
		selected_models = request.POST.getlist('models[]')
		email = email.lower()
		
		try:
			user = User.objects.get(id=user_id)
			user.first_name=name
			user.username=email
			user.email=email
			if status=="A":
				user.is_active = True
			else:
				user.is_active = False
			user.save()
	
			if role == 'super_admin':
				user.is_superuser = True
				user.is_staff = True
				user.groups.clear()
				permission_list = Permission.objects.all()
				user.user_permissions.set(permission_list)
				user.save()
			
			else:
				user.is_superuser = False
				user.groups.clear()
				group = Group.objects.get(id=role) 
				group.user_set.add(user)
				group.save()
				permission_list = Permission.objects.filter(content_type_id__in = selected_models)
				user.user_permissions.set(permission_list)
				user.save()

			if new_pass:
				if new_pass == repassword and new_pass!="" and repassword!="":
					user.set_password(new_pass)
					user.save()
					
				else:
					messages.error(request, 'Password does not match.')
					return HttpResponseRedirect('/login/edit_admin/'+str(user_id))

			messages.success(request, 'Staff entry successfully done.')
			return HttpResponseRedirect('/login/super_admin')
		except Exception as e:
			print(str(e))
			messages.error(request, 'Somthing Wrong')
			return HttpResponseRedirect('/login/edit_admin/'+str(user_id))


class DeleteAdmin(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "auth.view_user"
	def get(self, request, *args, **kwargs):
		user_id = kwargs.get('user_id')
		try:
			user = User.objects.get(id=user_id)
			user.delete()
			return HttpResponseRedirect('/login/super_admin')
			
		except Exception as e:
			print(str(e))
			return HttpResponseRedirect('/login/super_admin')


class AddStaff(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_user"
	template_name = 'admin_add_admin.html'
	
	def get(self, request, *args, **kwargs):
		print(request.user.user_permissions.all().values_list('codename', flat=True))
		group_list = Group.objects.all()
		model_list = ContentType.objects.exclude(app_label__in=["auth","contenttypes","sessions","social_django","admin"])
		return render(request,self.template_name,locals())


	def post(self,request,*args, **kwargs):
		name = request.POST.get('name')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		role = request.POST.get('role')
		status = request.POST.get('status')
		email = request.POST.get('email')
		selected_models = request.POST.getlist('models[]')  
		email = email.lower()
	
		try:
			User.objects.get(email=email)
			messages.error(request, 'User already exists with given email.')
			return HttpResponseRedirect('add_staff')
			
		except User.DoesNotExist:
			if password == confirm_password:
				user = User.objects.create_user(
					email=email,
					username=email,
					first_name=name
					)
			
				if role == 'super_admin':
					user.is_superuser = True
					user.groups.clear()
					user.is_staff = True
					if status=="A":
						user.is_active = True
					else:
						user.is_active = False
					user.set_password(password)
					user.save()
					permission_list = Permission.objects.all()
					user.user_permissions.set(permission_list)			
					user.save()
					messages.success(request, 'Staff entry successfully done.')
					return HttpResponseRedirect('add_staff')

				else:
					user.is_staff= True
					if status=="A":
						user.is_active = True
					else:
						user.is_active = False
					user.set_password(password)
					user.save()

					group = Group.objects.get(id=role) 
					group.user_set.add(user)
					group.save()
					permission_list = Permission.objects.filter(content_type_id__in = selected_models)
					user.user_permissions.set(permission_list)
					user.save()
					messages.success(request, 'Staff entry successfully done.')
					return HttpResponseRedirect('add_staff')
			else:
				messages.error(request, 'Password does not match.')
				return HttpResponseRedirect('add_staff')



class StaffList(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_user"
	template_name = 'admin_staff_list.html'
	def get(self, request, *args, **kwargs):
		users = User.objects.filter(is_staff=True).exclude(is_superuser=True)
		return render(request,self.template_name,locals())

	def post(self,request):
		value = request.POST.get('value')
		if value:
			user = User.objects.get(pk = value)
			if user.is_active:
				user.is_active = False
			else:
				user.is_active = True
			user.save()
		return HttpResponse(json.dumps({}),content_type = 'application/json')


class EditStaff(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_user"
	template_name = 'edit-staff.html'
	def get(self, request, *args, **kwargs):
		user_id = kwargs.get('user_id')
		user = User.objects.get(id=user_id)
		user_groups = user.groups.all()
		current_id = 0
		if user_groups:
			current_id = user_groups[0].id
		groups = Group.objects.all()
		model_items = ContentType.objects.exclude(app_label__in=["auth","contenttypes","sessions","social_django","admin"])
		selected_permissions = set(Permission.objects.filter(user=user_id).values_list('content_type__model',flat=True).distinct())
		model_list = map(lambda model_item: {"id":model_item.id,"name":model_item.name,"slug":(model_item.name).replace(" ","")}, model_items) 
		return render(request,self.template_name,locals())


	def post(self,request,*args, **kwargs):

		user_id = kwargs.get('user_id')
		name = request.POST.get('name')
		new_pass = request.POST.get('password')
		confirm_password = request.POST.get('repassword')
		role = request.POST.get('role')
		status = request.POST.get('status')
		email = request.POST.get('email')
		selected_models = request.POST.getlist('models[]')
		email = email.lower()
		
		try:
			user = User.objects.get(id=user_id)
			user.first_name=name
			user.username=email
			user.email=email
			if status=="A":
				user.is_active = True
			else:
				user.is_active = False
			user.save()
			if role == 'super_admin':
				user.is_superuser = True
				user.groups.clear()
				permission_list = Permission.objects.all()
				user.user_permissions.set(permission_list)
				user.save()
				
			else:
				user.is_staff = True
				user.groups.clear()
				group = Group.objects.get(id=role)
				group.user_set.add(user)
				group.save()
				permission_list = Permission.objects.filter(content_type_id__in = selected_models)
				user.user_permissions.set(permission_list)
				user.save()
		
			
			if new_pass:
				if new_pass == confirm_password and new_pass!="" and confirm_password!="":		
					user.set_password(new_pass)
					user.save()
					
				else:
					messages.error(request, 'Password does not match!!!!!!.')
					return HttpResponseRedirect('/login/edit_staff/'+str(user_id))
		
			messages.success(request, 'Staff entry successfully done.')
			return HttpResponseRedirect('/login/staff_list')	
		
		except Exception as e:
			print(str(e))
			messages.error(request, 'Somthing Wrong')
			return HttpResponseRedirect('/login/edit_staff/'+str(user_id))


# add group 
class AddRole(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_group"
	template_name = "admin_role.html"
	def get(self,request, *args, **kwargs):
		return render(request,self.template_name,locals())

	def post(self,request, *args, **kwargs):
		role = request.POST.get('role')
		try:
			group=Group.objects.get(name=role)
			messages.error(request,"Group already Exist.")
			return HttpResponseRedirect('/login/add_role')
		except Group.DoesNotExist:
			group = Group.objects.create(name=role) 
			group.save()
			messages.success(request,"Successfully Group create")
			return HttpResponseRedirect('/login/role_list')


class RoleList(PermissionRequiredMixin,StaffUserOnly,TemplateView):
	permission_required = "auth.view_group"
	template_name = "admin_role_list.html"

	def get(self,request, *args, **kwargs):
		groups = Group.objects.all()
		return render(request,self.template_name,locals())


class DeleteRole(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "auth.view_group"
	def get(self, request, *args, **kwargs):
		group_id = kwargs.get('group_id')
		try:
			group = Group.objects.get(id=group_id)
			group.delete()
			return HttpResponseRedirect('/login/role_list')
			
		except Exception as e:
			print(str(e))
			return HttpResponseRedirect('/login/role_list')
	

class EditRole(PermissionRequiredMixin,StaffUserOnly,View):
	permission_required = "auth.view_group"
	template_name = 'edit-role.html'
	def get(self, request, *args, **kwargs):
		group_id = kwargs.get('group_id')
		group = Group.objects.get(id=group_id)
		return render(request,self.template_name,locals())

	def post(self,request, *args, **kwargs):
		group_id = kwargs.get('group_id')
		role = request.POST.get('role')
		try:
			group = Group.objects.get(id=group_id)	
			group.name = role
			group.save()
			messages.success(request,"Successfully Update Role")	
			return HttpResponseRedirect('/login/role_list')

		except Exception as e:
			print(str(e))	
			messages.error(request,"Something Went Wrong")	
			return HttpResponseRedirect('/login/edit_role'+str(group_id))
