from .base import *


DEBUG = False

ALLOWED_HOSTS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": get_secret("DBUSER"),
        "PASSWORD": get_secret("DBPASSWORD"),
        "HOST": "postgresql",
        "PORT": "5432",
    }
}


CORS_ORIGIN_WHITELIST = []
CORS_ALLOW_CREDENTIALS = True
