from django.db import models
from authentication_user.models import Account


# Create your models here.

class Subscription(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    chargebee_subscription_id = models.CharField(max_length=25)
