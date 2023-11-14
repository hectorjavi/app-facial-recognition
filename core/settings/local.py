import os
from datetime import timedelta

from corsheaders.defaults import default_headers

from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CODIGO SECRETO"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers)

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

SQLite = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",  # noqa
}

DATABASES = {"default": SQLite}

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
