from django.apps import AppConfig


class EmailNotificationsConfig(AppConfig):
    name = 'email_notifications'
    verbose_name = 'Email Notifications'

    def ready(self):
        from . import signals  # noqa
