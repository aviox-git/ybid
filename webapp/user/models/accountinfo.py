from django.db import models
from django.contrib.auth.models import User

class AccountInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, null = True)
	company_name = models.CharField(max_length=100, blank=True,null=True)
	website = models.URLField(max_length=100, blank=True,null=True)
	strip_number = models.CharField(max_length=100,blank=True,null=True)
	phone = models.BigIntegerField(blank=True,null=True)
	zipcode = models.BigIntegerField(blank=True,null=True)
	company_logo = models.ImageField(blank=True, upload_to='accountinfo')
	business_license = models.FileField(blank=True, upload_to='accountinfo')
	about_seller = models.TextField(max_length=500,  blank=True,null=True)
	terms_condition = models.BooleanField(null=True,blank=True,default=False)

	def __str__(self):
		return self.user.username

	def get_latest_address(self):
		try:
			address = self.useraddress_set.latest('pk')
		except:
			address = {}
		return address

	def card_details(self):
		try:
			card = self.cardsinfo_set.latest('pk')
			card.credit_card_number = card.credit_card_number.strip()
			card.save()
			
		except:
			card = {}
		return card

class UserAddress(models.Model):
	info = models.ForeignKey(AccountInfo, blank=True, null=True, on_delete=models.CASCADE)
	billing_address = models.TextField(max_length=200,blank=True,null=True) 
	address = models.TextField(max_length=50,blank=True,null=True) 
	country = models.CharField(max_length=25, default = 'India')
	state = models.CharField(max_length=25, null = True)
	city = models.CharField(max_length=25,blank=True,null=True)


class CardsInfo(models.Model):
	info = models.ForeignKey(AccountInfo, null=True, on_delete=models.CASCADE)
	credit_card_number = models.CharField(max_length=25, null=True)
	expiration_date = models.CharField(max_length=10, null= True)