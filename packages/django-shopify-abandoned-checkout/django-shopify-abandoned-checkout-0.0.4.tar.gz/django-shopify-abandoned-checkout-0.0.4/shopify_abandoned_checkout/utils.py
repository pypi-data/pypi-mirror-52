from shopify import Session, ShopifyResource, Checkout
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from smtplib import SMTPException
import sys
import datetime

from .models import AbandonedCheckout

class AbandonedCheckoutHandler:
    def get_session(self):
        site = getattr(settings, 'SHOPIFY_ABANDONED_CHECKOUT_SITE', None)
        token = getattr(settings, 'SHOPIFY_ABANDONED_CHECKOUT_TOKEN', None)
        if site is None or token is None:
            use_session = getattr(settings, 'SHOPIFY_ABANDONED_CHECKOUT_USE_SYNC_SESSION', False)
            if use_session:
                from shopify_sync.models import Session as SyncSession
                session = SyncSession.objects.first()
                if session:
                    site = session.site
                    token = session.token
            
        return Session(site, '2019-04', token)
        
    def process_abandoned_carts(self):
        hours = getattr(settings, 'SHOPIFY_ABANDONED_CHECKOUT_HOURS_TO_WAIT', 10)
        session = self.get_session()
        ShopifyResource.activate_session(session)

        # 1 hour time range
        end_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
        start_time = end_time - datetime.timedelta(hours=1)

        data = Checkout.find(limit=250, updated_at_min=start_time, update_at_max=end_time)
        checkouts_with_emails = [a for a in data if a.email is not None]

        for checkout in checkouts_with_emails:
            obj, created = AbandonedCheckout.objects.get_or_create(
                checkout_id=checkout.id,
                user_email=checkout.email,
                checkout_url=checkout.abandoned_checkout_url,
            )
          
            if not obj.email_sent:
                try:
                    self.send_email(checkout)
                    obj.email_sent = True
                except SMTPException as e:
                    obj.email_errors = e
                obj.save()

    def send_email(self, checkout: Checkout):
        subject = getattr(settings, 'SHOPIFY_ABANDONED_CHECKOUT_SUBJECT', 'Abandoned Checkout')
        from_addr = settings.DEFAULT_FROM_EMAIL
        context = {'checkout': checkout}
        print(checkout)
        msg_plain = render_to_string('email/abandoned_checkout.txt', context)
        msg_html = render_to_string('email/abandoned_checkout.html', context)
        send_mail(
            subject,
            msg_plain,
            from_addr,
            [checkout.email],
            html_message=msg_html,
        )
