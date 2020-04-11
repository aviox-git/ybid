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


	class Meta:
		permissions = (
				('can_view_home', 'Home'),
				('can_view_super_admin', 'Super Admin'),
				('can_view_staff', 'Staff'),
				('can_add_staff', 'Add Staff'),
				('can_view_roles', 'Roles'),
				('can_view_users', 'Users'),
				('can_manage_content', 'Manage Content'),
				('can_view_blog_category', 'Blog Category'),
				('can_view_blogs', 'Blogs'),
				('can_view_config', 'Configuration'),
				('can_view_company_profile', 'Company Profile'),
				('can_view_faq_category', 'Faq Category'),
				('can_view_faqs', 'FAQs'),
				('can_view_price_and_fee', 'Price and Fee'),
				('can_view_manage_posting', 'Manage Posting'),
				('can_view_sales_order', 'Sales Order'),
				('can_view_order_history', 'Order History'),
				('can_view_contact_category', 'Contact Category'),
				('can_view_contact', 'Contact'),
				# ('can_view_refund_request', 'Refund Requests')
			)


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