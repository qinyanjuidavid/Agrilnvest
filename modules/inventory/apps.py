from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = _("Inventory")
    name = "modules.inventory"

    def ready(self):
        import modules.inventory.signals
