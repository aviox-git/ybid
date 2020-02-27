from django.db import models
from PIL import Image
# Create your models here.

class Page(models.Model):
	title = models.CharField(max_length=255,blank=True,null=True)
	content = models.TextField(blank=True,null=True)
	url=models.CharField(max_length=255,blank=True,null=True)
	background_image=models.ImageField(upload_to='pages',blank=True, null =True)
	status=models.BooleanField(default=True,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	delete_status=models.BooleanField(default=False,blank=True,null=True)
	def __str__(self):
		return self.title