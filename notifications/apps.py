from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        try:
            import notifications.signals
        except ImportError:
            pass
