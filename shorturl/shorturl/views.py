from urlparse import urljoin

from django.conf import settings
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from shorturl.models import ShortUrl


class LongUrlView(View):
    """
    request:
        http://localhost:8000/longurl/?long_url=www.baidu.com
    
    response:
        http://localhost:8000/su/<hashkey>
    """
    def get(self, request, *args, **kwargs):
        long_url = request.GET.get('long_url')
        if len(long_url) > 200:
            return HttpResponse(u'Url is too long, cannot continue.', status=401)
        if not long_url:
            return HttpResponse(u'Please input url.', status=401)
        if not request.GET.get('custom_url'):
            short_url_obj, _ = ShortUrl.objects.get_or_create(long_url=long_url, defaults={'long_url': long_url})
        else:
            custom_url = request.GET['custom_url']
            if len(custom_url) > 32:
                return HttpResponse(u'Custom url is too long, cannot continue.', status=401)
            if ShortUrl.decode_hashkey_to_id(custom_url):
                return HttpResponse(u'This custom key: %s is invalid, please try again' % custom_url, status=401)
            short_url_obj, _ = ShortUrl.objects.get_or_create(custom_url=custom_url,
                                                              defaults={'long_url': long_url,
                                                                        'custom_url': custom_url})
        return HttpResponse(urljoin(settings.SITE_URL, 'su/%s' % (short_url_obj.custom_url or short_url_obj.hashkey)))


class ShortUrlView(View):
    """
    request:
        http://localhost:8000/su/<hashkey>
    
    redirect:
        http://www.test123.com
    """
    def get(self, request, *args, **kwargs):
        hash_key = kwargs.get('hashkey')
        id = ShortUrl.decode_hashkey_to_id(hash_key)
        if id:
            qs = ShortUrl.objects.filter(id=id)
        else:
            qs = ShortUrl.objects.filter(custom_url=hash_key)
        if qs.exists():
            qs.update(access_count=(F('access_count')+1))
            return HttpResponseRedirect(urljoin(settings.HTTP_PREFIX, qs.first().long_url))

        return HttpResponse(u'Please input a valid short url.', status=401)
