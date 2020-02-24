from django.urls import path
from .views import PhotoUpload, MyAccountInfo
urlpatterns = [
	path('',MyAccountInfo.as_view(), name='my_account_info'),
	path('photo-upload',PhotoUpload.as_view(), name='photo_upload'),

]