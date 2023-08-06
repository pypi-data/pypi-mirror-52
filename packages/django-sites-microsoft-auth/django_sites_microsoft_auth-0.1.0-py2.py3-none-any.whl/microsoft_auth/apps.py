from django.apps import AppConfig


class MicrosoftAuthConfig(AppConfig):
    name = "microsoft_auth"
    verbose_name = "Microsoft Auth"

    def ready(self):
        import microsoft_auth.signals
