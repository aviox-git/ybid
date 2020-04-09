from django.db import models
from PIL import Image
# Create your models here.


POSTION_CHOICE = (('t', 'top'), ('b', 'bottom'))

class Page(models.Model):
	title = models.CharField(max_length=255,blank=True,null=True)
	content = models.TextField(blank=True,null=True)
	url=models.CharField(max_length=255,blank=True,null=True)
	background_image=models.ImageField(upload_to='pages',blank=True, null =True)
	status=models.BooleanField(default=True,blank=True,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	postion = models.CharField(max_length = 2, choices = POSTION_CHOICE, default="b")
	delete_status=models.BooleanField(default=False,blank=True,null=True)
	def __str__(self):
		return self.title


class ContactCategory(models.Model):
	category_name = models.CharField(max_length = 100)
	status = models.BooleanField(default = False)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.category_name 


class ContactUs(models.Model):
	created_on = models.DateTimeField(auto_now=True)
	category = models.ForeignKey(ContactCategory,on_delete = models.CASCADE,null=True)
	first_name = models.CharField(max_length=25,blank=True,null=True)
	last_name = models.CharField(max_length=25,blank=True,null=True)
	email = models.EmailField(max_length=25,blank=True,null=True)
	subject = models.CharField(max_length=25,blank=True,null=True)
	message = models.TextField(blank=True,null=True)
	inquiry = models.CharField(max_length=25,blank=True,null=True)

	def getReplies(self):
			reply = AdminReply.objects.filter(contact = self).order_by('created_on')
			return reply

	def getLatestReply(self):
		response = {}
		try:
			reply = AdminReply.objects.filter(contact = self).latest('pk')
			if reply.replied:
				response['status'] = True
				response['time'] = reply.created_on
			else:
				response['status'] = False

		except AdminReply.DoesNotExist:
			response['status'] = False
		return response



class AdminReply(models.Model):
	contact = models.ForeignKey(ContactUs, on_delete = models.CASCADE)
	created_on = models.DateTimeField(auto_now_add = True)
	message = models.TextField()
	replied = models.BooleanField(default = False)

class ContactAttachment(models.Model):
	contact = models.ForeignKey(ContactUs, on_delete = models.CASCADE)
	created_on = models.DateTimeField(auto_now_add = True)
	attachment = models.FileField(upload_to = 'contact/')


class AdminReplyAttachment(models.Model):
	reply = models.ForeignKey(AdminReply, on_delete = models.CASCADE)
	created_on = models.DateTimeField(auto_now_add = True)
	attachment = models.FileField(upload_to = 'contact/')