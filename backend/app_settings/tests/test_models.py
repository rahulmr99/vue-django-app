from app_settings.models import GeneralSettings


def test_creating_app_settings(db):
    g = GeneralSettings.create_app_settings()
    assert g.feedbackconfig.pk
    assert g.reminder.pk
    assert g.initialconfirmation.pk
