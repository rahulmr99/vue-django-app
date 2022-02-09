from django.contrib import admin
from calendar_manager.models import *


@admin.register(CalendarDb)
class CalendarDbAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_datetime', 'users_provider', 'start_datetime', 'end_datetime', 'is_unavailable', 'uid', 'remember']
