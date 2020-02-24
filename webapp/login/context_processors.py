from core.models import Config

def getDomain(request):
	try:
		site_name = Config.objects.latest('pk')
	except Exception as e:
		site_name = None

	return {
	'site_name': site_name,
	}