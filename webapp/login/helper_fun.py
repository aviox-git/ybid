from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages

# Staff User Mixin:  Allow Access Only to the Staff User

class StaffUserOnly(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            print('=======================')
        else:
        	messages.error(request,'You don\'t Have Permission To Access this,Please Login With Right Credentials')
        	return HttpResponseRedirect('/login/admin-login')
        return super().dispatch(request, *args, **kwargs)