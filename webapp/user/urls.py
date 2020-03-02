from django.urls import path
from .views import PhotoUpload, MyAccountInfo, ConfirmEmail
urlpatterns = [
	path('',MyAccountInfo.as_view(), name='my_account_info'),
	path('photo-upload',PhotoUpload.as_view(), name='photo_upload'),
	path('confirm/<slug:uidb64>/<slug:token>', ConfirmEmail.as_view(), name='confirm'),

]