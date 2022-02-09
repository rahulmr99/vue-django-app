from django.apps import AppConfig


class OpenvbxConfig(AppConfig):
    name = 'openvbx'

    def ready(self):
        import openvbx.signals