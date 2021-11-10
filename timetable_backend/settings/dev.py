from .base import *


DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost:3001",
]
CORS_ALLOW_CREDENTIALS = True
