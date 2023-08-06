from django.db import models

class AbandonedCheckout(models.Model):
  checkout_id = models.BigIntegerField(unique=True)
  checkout_url = models.CharField(max_length=255, unique=True)
  user_email = models.EmailField()
  email_sent = models.BooleanField(default=False)
  email_errors = models.TextField()
  created_at = models.DateField(auto_now_add=True)
  modified_at = models.DateField(auto_now=True)

  def __str__(self):
    return self.user_email + " - " + self.checkout_id.__str__()
