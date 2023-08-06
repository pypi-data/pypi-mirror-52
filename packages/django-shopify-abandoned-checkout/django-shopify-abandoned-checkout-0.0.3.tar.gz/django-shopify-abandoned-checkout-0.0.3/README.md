# django-shopify-abandoned-checkout

Shopify's abandoned checkout email feature does not work when in use with the Shopify storefront API. This is a workaround to generate abandoned checkout emails using the Shopify admin API. It works standalone and with django-shopify-sync

# Install

1. `pip install django-shopify-abandoned-checkout`
2. Add `shopify_abandoned_checkout` to `INSTALLED_APPS`
3. In settings, set either the site and token or the use sync sesion.

Set the following settings

- SHOPIFY_ABANDONED_CHECKOUT_SITE - Shopify site name. If your store's url is example.myshopify.com then your store name is example.
- SHOPIFY_ABANDONED_CHECKOUT_TOKEN - Shopify app token
- SHOPIFY_ABANDONED_CHECKOUT_USE_SYNC_SESSION - (default False) If using django-shopify-sync, you may set this to True to use the first session object for authentication
- SHOPIFY_ABANDONED_CHECKOUT_HOURS_TO_WAIT - (default 10) set the number of hours to wait before sending the email.
- SHOPIFY_ABANDONED_CHECKOUT_SUBJECT - (default: Abandoned Checkout) the subject line for emails

## Email templates

Override the html and txt email templates in `email/abandoned_checkout.html` and `email/abandoned_checkout.txt`. The context includes a Shopify Checkout object. See https://help.shopify.com/en/api/reference/orders/abandoned-checkouts

There are default templates to get started but they are not intended to be used as is.

# Usage

This module includes a management command and celery task both named send_shopify_abandoned_checkouts. You may also call it directly or even extend the handler class.

```
from shopify_abandoned_checkout.utils import AbandonedCheckoutHandler
handler = AbandonedCheckoutHandler()
handler.process_abandoned_carts()
```

# Testing

Sadly there is no demo shopify store to use for tests with a real backend. To test, enter your store credentials in sandbox/settings.py and then run `./manage.py test`
