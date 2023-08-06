from django.test import TestCase
from django.core import mail
from django.conf import settings
from shopify_sync.models import Session as SyncSession
from .utils import AbandonedCheckoutHandler


class AbandonTestCase(TestCase):
    def test_get_carts(self):
        handler = AbandonedCheckoutHandler()
        handler.process_abandoned_carts()
        self.assertGreaterEqual(len(mail.outbox), 1)
    
    def test_usage_with_django_shopify_sync(self):
        site = settings.SHOPIFY_ABANDONED_CHECKOUT_SITE
        token = settings.SHOPIFY_ABANDONED_CHECKOUT_TOKEN
        SyncSession.objects.create(site=site, token=token)

        with self.settings(SHOPIFY_ABANDONED_CHECKOUT_SITE=None):
            handler = AbandonedCheckoutHandler()
            handler.process_abandoned_carts()
