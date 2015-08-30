"""
WSGI config for myfarmreport project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.sys.path.append(os.path.join(os.path.dirname(__file__), './../'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myfarmreport.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
