from django.core.management.base import BaseCommand
from shopify_abandoned_checkout.utils import AbandonedCheckoutHandler

class Command(BaseCommand):
    help = 'Checks for any abandoned carts'

    def handle(self, *args, **options):
        handler = AbandonedCheckoutHandler()
        handler.process_abandoned_carts()
