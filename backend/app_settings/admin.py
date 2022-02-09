from django.contrib import admin
from django.shortcuts import redirect

from .models import *


@admin.register(WorkingPlan)
class WorkingPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'users', 'enable', 'day', 'start', 'end']


@admin.register(GeneralSettings)
class GeneralSettingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name']


@admin.register(InitialConfirmation)
class InitialConfirmationAdmin(admin.ModelAdmin):
    list_display = ['id', 'email_subject']


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['id', 'email_subject', 'send_time']


@admin.register(FeedbackConfig)
class FeedbackConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailDashboard)
class EmailDashboardAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('/admin/email-dashboard/')
