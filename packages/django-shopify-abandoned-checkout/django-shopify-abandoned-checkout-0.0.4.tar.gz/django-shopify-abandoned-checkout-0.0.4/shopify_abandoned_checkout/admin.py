from django.contrib import admin
from .models import AbandonedCheckout

@admin.register(AbandonedCheckout)
class AbandonedCheckoutAdmin(admin.ModelAdmin):
    fields = ('id', 'checkout_id', 'checkout_url', 'user_email', 'email_sent', 'email_errors', 'created_at', 'modified_at')
    readonly_fields = ('id', 'checkout_id', 'checkout_url', 'user_email', 'email_errors', 'created_at', 'modified_at')
    list_display = ('checkout_id', 'user_email', 'email_sent')
