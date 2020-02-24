from django.contrib import admin
from .models.core import Config, Company

# Register your models here.
admin.site.register(Config)
admin.site.register(Company)
