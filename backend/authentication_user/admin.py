from django.contrib import admin
from . import models


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = [
        'generalsettings__company_name', 'username', 'name', 'last_name', 'email', 'phone', 'note',
    ]
    list_display = [
        'generalsettings', 'username', 'name', 'last_name', 'email', 'phone', 'note', 'is_active', 'is_admin',
        'is_provider', 'is_secretarie', 'is_root_user',
    ]
    list_select_related = ['generalsettings', ]
    list_filter = ['is_provider', 'is_admin', 'is_customers', 'is_active', 'is_root_user', ]


@admin.register(models.GoogleCredentials)
class CredentialsModelAdmin(admin.ModelAdmin):
    pass
