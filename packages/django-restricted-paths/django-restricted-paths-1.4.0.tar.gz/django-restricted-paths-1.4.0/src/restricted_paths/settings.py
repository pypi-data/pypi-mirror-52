from django.conf import settings

SETTINGS = getattr(settings, "RESTRICTED_PATHS", {})

ENABLED = SETTINGS.get("ENABLED", True)

PATHS = SETTINGS.get("PATHS", ())

VIEW = SETTINGS.get("VIEW", None)
