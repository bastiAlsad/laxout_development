from django.apps import AppConfig


class LaxoutAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laxout_app'
    

    def ready(self):
        import laxout_app.signals