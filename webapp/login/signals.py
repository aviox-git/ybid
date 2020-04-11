  
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from user.models import AccountInfo, UserAddress
from django.dispatch import receiver

@receiver(post_save, sender = User)
def save_profile(sender, instance, created, **kwargs):
	if created:

		account_info, createinfo = AccountInfo.objects.get_or_create(user = instance, terms_condition = True)
		if createinfo:
			UserAddress.objects.create(info = account_info)

post_save.connect(save_profile, sender=User)