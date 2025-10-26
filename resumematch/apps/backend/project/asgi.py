import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Initialize DI on startup
try:
    from src.di.container import container  # noqa: F401
except Exception:
    # Allow startup without full DI (e.g., during migrations)
    pass

application = get_asgi_application()