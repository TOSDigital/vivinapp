from django.apps import AppConfig


class AttandanceConfig(AppConfig):
    name = 'attandance'

    def ready(self):
        import attandance.signals  # noqa
        import attandance.handlers 