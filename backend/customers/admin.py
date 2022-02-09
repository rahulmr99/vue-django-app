from django.contrib import admin
from customers.models import *


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name']
