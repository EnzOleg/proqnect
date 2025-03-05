"""
WSGI config for proqnect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proqnect.settings')

application = get_wsgi_application()

logger = logging.getLogger(__name__)
logger.info("Запущено через WSGI: %s", application)
