import os
from datetime import timedelta

from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=120),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

POSTGRES_DB = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "HOST": os.environ.get("POSTGRES_HOST"),
    "PORT": os.environ.get("POSTGRES_PORT"),
    "USER": os.environ.get("POSTGRES_USER"),
    "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "NAME": os.environ.get("POSTGRES_DB_NAME"),
}

DATABASES = {"default": POSTGRES_DB}

STATIC_ROOT = BASE_DIR / "staticfiles"  # noqa

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


DBBACKUP_FILENAME_TEMPLATE = "{datetime}.sql"
DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {"location": BASE_DIR / "backup"}  # noqa


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
