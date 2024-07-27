import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE","djshop.envs.development")
application = get_wsgi_application()
