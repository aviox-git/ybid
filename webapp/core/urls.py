from django.urls import path
from .views import GeneralConfigView, CompanyProfile

urlpatterns = [
	path('', GeneralConfigView.as_view(),name='admin_config' ),
	path('comapny-profile', CompanyProfile.as_view(),name='company_profile' ),
]
