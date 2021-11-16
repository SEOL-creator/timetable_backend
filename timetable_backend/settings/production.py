from .base import *
import os


DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    "api.classtime.kro.kr",
]


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

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)


CORS_ORIGIN_WHITELIST = ["https://classtime.kro.kr"]
CORS_ALLOW_CREDENTIALS = True


STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR.parent, "nginx_root", "static"))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR.parent, "nginx_root", "media"))
