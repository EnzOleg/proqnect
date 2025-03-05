import os
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proqnect.settings')

from django.conf import settings
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
print("Импортируем chat.routing...")
import chat.routing


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

logger = logging.getLogger(__name__)
logger.info("Запущено через ASGI: %s", application)

if settings.DEBUG:
    from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
    application = ASGIStaticFilesHandler(application)
