from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from core.models import Config,Company
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin


class GeneralConfigView(View):
	template_name = 'admin_config.html'

	def get(self,request):
		try:
			config = Config.objects.latest('pk')
		except Config.DoesNotExist:
			pass
		return render(request,self.template_name,locals())

	def post(self,request):

		if settings.CAN_UPDATE_SETTINGS == 1:
			maintaince_mode = request.POST.get('maintaince_mode')
			site_name = request.POST.get('site_name')
			site_url = request.POST.get('site_url')
			description = request.POST.get('description')
			tags = request.POST.get('tags')
			youtube = request.POST.get('youtube')
			facebook = request.POST.get('facebook')
			twitter = request.POST.get('twiiter')
			google = request.POST.get('google')
			files = request.FILES.get('logo')

			try:
				config = Config.objects.latest('pk')
				config.site_name = site_name
				config.description = description
				config.site_url = site_url
				config.tags = tags
				config.url_youtube_promo_video = youtube
				config.facebook_username = facebook
				config.twitter_username = twitter
				config.google_recaptcha_public_key = google
				print(config.url_youtube_promo_video,config.facebook_username,config.twitter_username,config.google_recaptcha_public_key,'------------------------')
				if files:
					config.logo = files

				else:
					config.logo = config.logo

				if maintaince_mode == 'yes':
					config.maintaince_mode = True
				else:
					config.maintaince_mode = False

				config.save()
			except Config.DoesNotExist:
				config = Config()

				config.site_name = site_name
				config.description = description
				config.site_url = site_url
				config.tags = tags
				config.url_youtube_promo_video = youtube
				config.facebook_username = facebook
				config.twitter_username = twitter
				config.google_recaptcha_public_key = google

				files = request.FILES.get('logo')
				if files:
					config.logo = files
				if maintaince_mode == 'yes':
					config.maintaince_mode = True
				else:
					config.maintaince_mode = False
				config.save()
		return HttpResponseRedirect('/core/')

class CompanyProfile(View):
	template_name = 'admin_company_profile.html'
	def get(self,request):
		try:
			company = Company.objects.latest('pk')
		except Company.DoesNotExist:
			pass
		return render(request,self.template_name,locals())


	def post(self,request):
		company_name = request.POST.get('company_name')
		address = request.POST.get('address')
		city = request.POST.get('city')
		state = request.POST.get('state')
		zip_code = request.POST.get('zip')
		phone = request.POST.get('phone')
		email = request.POST.get('email')
		profile = request.FILES.get('img')

		try:
			company = Company.objects.latest('pk')
			company.company_name = company_name
			company.address = address
			company.city = city
			company.state = state
			company.zip_code = zip_code
			company.telephone = phone
			company.email = email
			if profile:
				company.profile_picture = profile
			else:
				company.profile_picture = company.profile_picture
			company.save()

		except Company.DoesNotExist:
			company = Company()
			company.company_name = company_name
			company.address = address
			company.city = city
			company.state = state
			company.zip_code = zip_code
			company.telephone = phone
			company.email = email
			company.profile_picture = profile
			company.save()

		return HttpResponseRedirect('/core/comapny-profile')


