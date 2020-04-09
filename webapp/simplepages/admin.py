from django.contrib import admin
from simplepages.models import FAQCategory, FAQ, BlogCategory, Blog,Page, ContactCategory, ContactUs, AdminReply, ContactAttachment, AdminReplyAttachment

# Register your models here.
admin.site.register(FAQCategory)
admin.site.register(FAQ)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Page)
admin.site.register(ContactCategory)
admin.site.register(ContactUs)
admin.site.register(AdminReply)
admin.site.register(ContactAttachment)
admin.site.register(AdminReplyAttachment)
