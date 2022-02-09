from django.db import models


class AccountQuerySet(models.QuerySet):
    def providers(self):
        return self.filter(is_provider=True)

    def customers(self):
        return self.filter(is_customers=True)

    def authorizables(self):
        return self.filter(models.Q(is_admin=True) | models.Q(is_provider=True))
