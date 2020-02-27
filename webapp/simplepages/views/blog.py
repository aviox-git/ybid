from django.shortcuts import render
from django.views.generic import TemplateView, View
from simplepages.models import BlogCategory,Blog
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect,HttpResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from login.helper_fun import StaffUserOnly
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

# ============= Blog Categories ============== #
class BlogCategoriesView(StaffUserOnly,View):
	# permission_required = "simplepages.view_blogcategory"
	def get(self,request):
		blog_cats = BlogCategory.objects.all()
		return render(request,'admin_blog-categories.html',locals())
	# Delete the FAQ 
	def post(self,request):
		cat_id = request.POST.get('cat_id')
		BlogCategory.objects.get(pk = cat_id).delete()
		response = {}
		return HttpResponse(json.dumps(response), content_type="application/json")

class BlogCategoriesAddView(StaffUserOnly,View):
	# permission_required = "simplepages.view_blogcategory"
	def get(self,request):
		return render(request,'admin_blog-category-add.html',locals())

	def post(self,request):
		status =  request.POST.get('status')
		order =  request.POST.get('order')
		category =  request.POST.get('category')

		if status and category and order:
			cat = BlogCategory(category_name = category,sort_order = order)
			if status == 'active':
				cat.status = True
			cat.save()
			messages.success(request,'Blog Category Successfully Added')
		else:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/blog-category')

class BlogCategoriesEditView(StaffUserOnly, View):
	# permission_required = "simplepages.view_blogcategory"
	def get(self, request,cat_id):
		cat = BlogCategory.objects.get(pk = cat_id)
		return render(request,'admin_blog-category-edit.html',locals())

	def post(self,request,cat_id):
		cat_id = cat_id
		status =  request.POST.get('status')
		order =  request.POST.get('order')
		name =  request.POST.get('category')
		try:
			if cat_id:
				category = BlogCategory.objects.get(pk = cat_id)
				if name:
					category.category_name = name
				if order:
					category.sort_order = order
				if status == 'active':
					category.status = True
				else:
					category.status = False
				category.save()
				messages.success(request,'Blog Category Successfully Added')
			else:
				messages.error(request,'Something Went Wrong')
		except Exception as e:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/blog-category')

# ===================== Blogs ======================= #
class BlogWebView(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = 'public_blog.html'

	def get(self, request, *args, **kwargs):
		page = request.GET.get('page', 1)
		cate = request.GET.get('category')
		categories = BlogCategory.objects.filter(status = True).order_by('-sort_order')
		
		if cate:
			if cate == 'all':
				blogs = Blog.objects.filter(status = True).order_by('-sort_order')
			else:
				blogs = Blog.objects.filter(category__id = cate,status = True).order_by('-sort_order')
		else:
			blogs = Blog.objects.filter(status = True).order_by('-sort_order')
		paginator = Paginator(blogs, 8)

		try:
			blogs = paginator.page(page)
		except PageNotAnInteger:
			blogs = paginator.page(1)
		except EmptyPage:
			blogs = paginator.page(paginator.num_pages)
		return render(request,self.template_name,locals())


class SingleBlog(LoginRequiredMixin, View):
	login_url = '/login/'
	template_name = 'public_blog_detail.html'
	def get(self, request, blog_id):
		blog = Blog.objects.get(pk = blog_id)
		return render(request,self.template_name,locals())


class BlogView(View):
	# permission_required = "simplepages.view_blog"
	def get(self,request):
		blogs = Blog.objects.all()
		return render(request,'admin_blogs.html',locals())

	# Delete the blog 
	def post(self,request):
		blog_id = request.POST.get('blog_id')
		Blog.objects.get(pk = blog_id).delete()
		response = {}
		return HttpResponse(json.dumps(response), content_type="application/json")

class AddBlogView(StaffUserOnly,View):
	# permission_required = "simplepages.view_blog"
	def get(self,request):
		category = BlogCategory.objects.all()
		return render(request,'admin_blog-add.html',locals())

	def post(self,request):
		category_id = request.POST.get('category')
		title = request.POST.get('title')
		order = request.POST.get('order')
		status = request.POST.get('status')
		description = request.POST.get('description')
		image = request.FILES.get('image') 
		if category_id and title and description:
			blog = Blog(category_id = category_id, author= request.user,image= image, title = title, description = description)
			if status == 'active':
				blog.status = True
			if order:
				blog.sort_order = order
			blog.save()
		messages.success(request,'Successfully Blog Added.')
		return HttpResponseRedirect('/blogs')

class EditBlogView(StaffUserOnly,View):
	# permission_required = "simplepages.view_blog"
	def get(self,request, blog_id):
		category = BlogCategory.objects.all()
		blog = Blog.objects.get(pk = blog_id)
		return render(request,'admin_blog-edit.html',locals())

	def post(self,request,blog_id):
		blog_id = blog_id
		category_id = request.POST.get('category')
		title = request.POST.get('title')
		order = request.POST.get('order')
		status = request.POST.get('status')
		description = request.POST.get('description')
		image = request.FILES.get('image')
		try:
			if blog_id:
				blog = Blog.objects.get(pk = blog_id)
				if category_id:
					category = BlogCategory.objects.get(pk = category_id)
					blog.category = category
				if order:
					blog.sort_order = order
				if status == 'active':
					blog.status = True
				else:
					blog.status = False
				if title:
					blog.title = title
				if description:
					blog.description = description
				if image:
					blog.image = image
				blog.save()
				messages.success(request,'Blog Successfully Updated')
			else:
				messages.error(request,'Something Went Wrong')
		except Exception as e:
			messages.error(request,'Something Went Wrong')
		return HttpResponseRedirect('/blogs')
