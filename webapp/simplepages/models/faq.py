from django.db import models

# Create your models here.
class FAQCategory(models.Model):
	category_name = models.CharField(max_length = 100)
	sort_order = models.PositiveIntegerField()
	status = models.BooleanField(default = False)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.category_name + " : " + str(self.sort_order)

	def getFAQ(self):
		faq = FAQ.objects.filter(category = self, status = True).order_by('-sort_order')
		return faq

class FAQ(models.Model):
	category = models.ForeignKey(FAQCategory,on_delete = models.CASCADE)
	question = models.TextField()
	answer = models.TextField()
	sort_order = models.PositiveIntegerField()
	status = models.BooleanField(default = False)
	created_on = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return  self.question