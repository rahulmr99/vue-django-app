from django.apps import AppConfig


class LexbotConfig(AppConfig):
    name = 'lexbot'

    def ready(self):
        # noinspection PyUnresolvedReferences
        from . import signals
