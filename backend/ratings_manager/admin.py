from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from ratings_manager.views import ReportsView
from .models import *


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['calendardb', 'rating_given', 'content', 'created_on', ]
    actions = ['see_reports']

    class Meta:
        ordering = ['-updated_on', ]

    def see_reports(self, request, queryset):
        return redirect(reverse('feedback:reports'))
