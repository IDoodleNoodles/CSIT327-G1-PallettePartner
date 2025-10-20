from django.apps import AppConfig

class PallateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pallattepartner.pallate'

    def ready(self):
        import pallattepartner.pallate.signals