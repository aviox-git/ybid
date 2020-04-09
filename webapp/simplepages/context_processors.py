from simplepages.models import Page
from django.conf import settings

def getPages(request):
	pages=Page.objects.filter(delete_status=False,status=True)
	return {
	'dynamic_pages':pages,
	'stripe_client_id': settings.STRIPE_CLIENT_ID
	}