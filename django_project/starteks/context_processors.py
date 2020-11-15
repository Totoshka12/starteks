

def site_name(request):
    from django.conf import settings
    return {'shop_name': settings.SHOP_NAME}
