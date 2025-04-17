from django.apps import AppConfig

class CappConfig(AppConfig):
    name = 'capp'
    def ready(self):
        import capp.signals
