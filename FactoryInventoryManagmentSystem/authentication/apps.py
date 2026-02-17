from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    # this runs when django starts
    def ready(self):

        # import signals so they activate
        import authentication.signals
