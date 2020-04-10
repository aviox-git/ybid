from django.shortcuts import render
from django.views.generic import View



class Events(View):
	template_name = 'public_multple_event_list.html'

	def get(self, request, *args, **kwargs):
		return render(request,self.template_name,{})


