from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "example_contacts.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import example_contacts.users.signals  # noqa: F401
        except ImportError:
            pass
