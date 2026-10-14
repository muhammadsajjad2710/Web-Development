"""
WSGI config for awan_rental project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awan_rental.settings')

application = get_wsgi_application()
