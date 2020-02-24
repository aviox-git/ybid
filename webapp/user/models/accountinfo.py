from django.db import models
from django.contrib.auth.models import User

class AccountInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, null = True)
	terms_condition = models.BooleanField(null=True,blank=True,default=False)

	def __str__(self):
		return self.user.username

class UserAddress(models.Model):
	info = models.ForeignKey(AccountInfo, blank=True, null=True, on_delete=models.CASCADE)
	country = models.CharField(max_length=25, default = 'India')
	state = models.CharField(max_length=25, null = True)