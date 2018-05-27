from django.test import TestCase

from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment
from django.test.client import Client

# from .models import ShortUrl

# setup_test_environment()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def get_data(self, url, data=None, **extra):
        return self.client.get(url, data=data, **extra)


class LongUrlViewTestCase(BaseTestCase):
    def test_success(self):
        resp = self.get_data(reverse("long_url"), data={'long_url': 'test.com'})
        self.assertEqual(resp.status_code, 200)

    def test_invalid_url_fail(self):
        resp = self.get_data(reverse("long_url"), data={'long_url': 'test.com', 'custom_url': 'peyQej'})
        self.assertEquals(resp.status_code, 401)

    def test_long_url_fail(self):
        resp = self.get_data(reverse("long_url"), data={'long_url': 't'*201})
        self.assertEquals(resp.status_code, 401)

    def test_long_custom_fail(self):
        resp = self.get_data(reverse("long_url"), data={'long_url': 'test.com', 'custom_url': 't'*33})
        self.assertEquals(resp.status_code, 401)


class ShortUrlViewTestCase(BaseTestCase):
    def test_success(self):
        self.get_data(reverse("long_url"), data={'long_url': 'www.google.com'})
        resp = self.get_data(reverse("short_url", kwargs={'hashkey': 'peyQej'}))
        self.assertEqual(resp.status_code, 302)

    def test_fail(self):
        resp = self.get_data(reverse("short_url", kwargs={'hashkey': 'peyQej123'}))
        self.assertEqual(resp.status_code, 401)
