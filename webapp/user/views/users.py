from django.shortcuts import render
from django.views.generic import View


class MyAccountInfo(View):
	template_name = 'public_account_info.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})

class PhotoUpload(View):
	template_name = 'public_photographer_upload.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})