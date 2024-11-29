from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

class UsersConfig(AppConfig):
    name = 'authentication'

    def ready(self):
        import authentication.signals
