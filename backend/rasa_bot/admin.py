from django.contrib import admin
from rasa_bot.models import RasaBotUserSession

class RasaBotUserSessionAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(RasaBotUserSession, RasaBotUserSessionAdmin)
