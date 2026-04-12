import os
import dj_database_url
from .settings import *

DEBUG = False

RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

ALLOWED_HOSTS = [
    RENDER_HOST,
    "localhost",
    "127.0.0.1"
] if RENDER_HOST else ["*"]

CSRF_TRUSTED_ORIGINS = [
    f"https://{RENDER_HOST}"
] if RENDER_HOST else []

SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600
    )
}

# FIXED STORAGE
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}