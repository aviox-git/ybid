from core.models import Config

def getPublic_Config(request):
    try:
        public = Config.objects.latest('pk')
    except Exception as e:
        public = Config.objects.create(url_youtube_promo_video = "https://youtube.com",tags = '#demo',maintaince_mode = True,logo = "default.png")


    return {
    'public_site_name': public.site_name,
    'public_description' : public.description,
    'public_logo' : public.logo,
    'public_fb_url' :  public.getSocialNetworkFullUrl('facebook'), 
    'public_twitter_url' : public.getSocialNetworkFullUrl('twitter'),    
    'public_google_recpatcha_key' :  public.google_recaptcha_public_key,   
    }
