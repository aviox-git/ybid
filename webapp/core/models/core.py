from django.db import models

# Create your models here.

class Config(models.Model):

	site_name = models.CharField(max_length = 60, default = "Site Name")
	description = models.TextField(default = "Description of site")
	domain_name = models.CharField(max_length = 18, default = "Domain.com")
	site_url = models.URLField(default = "https://Domain.com")
	tags = models.CharField(max_length = 2000)
	url_youtube_promo_video = models.URLField()
	facebook_username = models.CharField(max_length = 12, null= True, blank = True)
	twitter_username = models.CharField(max_length = 12, null= True, blank = True)
	google_recaptcha_public_key =  models.CharField(max_length = 100, null= True, blank = True)
	logo = models.ImageField(upload_to = 'logo')
	maintaince_mode = models.BooleanField()

	# core.models.Config.objects.latest('pk').getSocialNetworkFullUrl('facebook')

	def getSocialNetworkFullUrl (self, name):
	
		facebook_base = "https://facebook.com/"
		twitter_base = "https://twitter.com/"

		response = False

		if name == 'facebook' :
			if self.facebook_username:
				response =  facebook_base + self.facebook_username
		if name == 'twitter' :
			if self.twitter_username:
				response =  twitter_base + self.twitter_username
		
		return response


	def __str__(self):
		return self.site_name


class Company(models.Model):

	company_name = models.CharField(max_length = 250, default = "Company Name")
	address = models.CharField(max_length = 250)
	city = models.CharField(max_length = 250)
	state = models.CharField(max_length = 250)
	zip_code = models.CharField(max_length = 10)
	telephone = models.CharField(max_length = 25)
	email = models.EmailField()
	profile_picture = models.ImageField(upload_to = 'company_profile')
	 
	def __str__(self):
		return self.company_name