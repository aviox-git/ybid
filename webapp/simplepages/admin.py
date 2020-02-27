from django.contrib import admin
from simplepages.models import FAQCategory, FAQ, BlogCategory, Blog,Page

# Register your models here.
admin.site.register(FAQCategory)
admin.site.register(FAQ)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Page)