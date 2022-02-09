from rest_framework.routers import DefaultRouter

from app_settings.viewsets import (WorkingPlanModelViewSet, BreaksModelViewSet, GeneralSettingsModelViewSet,
                                   InitialConfirmationModelViewSet, ReminderModelViewSet,
                                   ReschedulingSettingsModelViewSet, CancellationSettingsModelViewSet, )
from authentication_user.viewsets import AccountModelViewSet, CustomersModelViewSet
from calendar_manager.viewsets import CalendarDbModelViewSet
from openvbx.viewsets import VoiceMailViewset, VoiceMailConfigViewset
from ratings_manager.viewsets import FeedbackConfigModelViewSet, FeedbackModelViewSet
from services.viewsets import ServiceModelViewSet, CategoryModelViewSet
from lexbot.viewsets import VoiceBotConfigViewset

router = DefaultRouter()

# only the signup is not protected
router.register(r'users', AccountModelViewSet)
router.register(r'customers', CustomersModelViewSet)
#  unprotected URLs - put the generalsettings_id in the url path itself to secure
router.register(r'calendar', CalendarDbModelViewSet, base_name='calendardb')

# safe URLs
router.register(r'service', ServiceModelViewSet)
router.register(r'service_category', CategoryModelViewSet)
router.register(r'working_plan', WorkingPlanModelViewSet)
router.register(r'breaks', BreaksModelViewSet)
router.register(r'general_settings', GeneralSettingsModelViewSet)
router.register(r'initial_confirmation', InitialConfirmationModelViewSet)
router.register(r'reschedule_settings', ReschedulingSettingsModelViewSet)
router.register(r'cancellation_settings', CancellationSettingsModelViewSet)
router.register(r'reminder', ReminderModelViewSet)
router.register(r'ratings_settings', FeedbackConfigModelViewSet)
router.register(r'voicemail', VoiceMailViewset)
router.register(r'voicemail_config', VoiceMailConfigViewset)
router.register(r'voicebot_config', VoiceBotConfigViewset)
router.register(r'feedback', FeedbackModelViewSet)

from .apps import ApiV1Config

app_name = ApiV1Config.name

urlpatterns = router.urls
