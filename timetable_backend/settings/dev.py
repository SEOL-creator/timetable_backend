from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "172.20.10.3"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://172.20.10.3:3000",
]
CORS_ALLOW_CREDENTIALS = True


MEDIA_URL = "http://localhost:8000/media/"
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "media"))
