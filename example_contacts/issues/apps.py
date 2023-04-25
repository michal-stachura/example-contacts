from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class IssuessConfig(AppConfig):
    name = "example_contacts.issues"
    verbose_name = _("Issues")

    def ready(self):
        try:
            import hades_star_backend.members.signals  # noqa F401
        except ImportError:
            pass
