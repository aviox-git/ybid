from django.db import models
from django.contrib.auth.models import User

class BlogCategory(models.Model):
	category_name = models.CharField(max_length = 100)
	sort_order = models.PositiveIntegerField()
	status = models.BooleanField(default = False)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.category_name + " : " + str(self.sort_order)

class Blog(models.Model):
	category = models.ForeignKey(BlogCategory,on_delete = models.CASCADE)
	author = models.ForeignKey(User,on_delete = models.CASCADE, null= True)
	image = models.ImageField(upload_to = 'blogs', default = "no-image.png")
	title = models.CharField(max_length = 250)
	description = models.TextField()
	sort_order = models.PositiveIntegerField()
	status = models.BooleanField(default = False)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return  self.title
