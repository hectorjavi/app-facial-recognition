import os
from datetime import timedelta

from corsheaders.defaults import default_headers

from ..logging import *  # noqa
from .base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS "get by environ split(" ")"
ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "Api-Key-Music",
]

# Deshabilitar CSRF 403 django admin "get by environ split(" ")""
CSRF_TRUSTED_ORIGINS = ["https://app-music-ia-production.up.railway.app"]

# HTTPS configure
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


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


# Mediafiles AWS S3
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_EXPIRE = os.environ.get("AWS_QUERYSTRING_EXPIRE")
AWS_S3_CUSTOM_DOMAIN = os.environ.get("AWS_S3_CUSTOM_DOMAIN")
# End Mediafiles AWS S3

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
