from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ForgetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='Code')
    def __str__(self):
        name = self.user.first_name + self.user.last_name
        return name
