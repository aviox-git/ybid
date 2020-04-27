from django.db import models

# Create your models here.

SERVICE_TYPE = (('self_portrait','Self Portrait'),('pro_portrait','Pro Portrait'),('self_free','Self Portrait - Free Trail'),('pro_free','Pro Portrait - Free Trail'))

class Prices(models.Model):

	package = models.CharField(max_length = 250)
	service_type = models.CharField(max_length = 20, choices = SERVICE_TYPE, default='self_portrait')
	special_fee = models.FloatField(default=20)
	special_minimum_students = models.FloatField(default=20)
	regular_fee = models.FloatField(default=30)
	regular_minimum_students = models.FloatField(default=20)
	discount = models.FloatField(null = True)
	minimum_students = models.FloatField(default=20)
	code = models.CharField(max_length = 250,null=True)
	expire_date = models.DateField(null = True)

	def __str__(self):
		return self.package