from celery import shared_task
from .utils import AbandonedCheckoutHandler

@shared_task
def send_shopify_abandoned_checkouts():
    handler = AbandonedCheckoutHandler()
    handler.process_abandoned_carts()