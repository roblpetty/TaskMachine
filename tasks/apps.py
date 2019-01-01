from django.apps import AppConfig


class tasksConfig(AppConfig):
    name = 'tasks'

    def ready(self):
        import tasks.signals