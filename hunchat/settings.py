"""
Django settings for hunchat project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import json
import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
import django_heroku
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(verbose=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if os.environ.get("DEBUG", "False") == "True":
    DEBUG = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

ALLOWED_HOSTS = json.loads(os.environ.get("ALLOWED_HOSTS"))

BUGSNAG = {
    "api_key": os.environ.get("BUGSNAG_API_KEY"),
    "project_root": BASE_DIR,
}


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_serializer_extensions",
    "drf_yasg",
    "generic_relations",
    "oauth2_provider",
    "social_django",
    "rest_framework_social_oauth2",
    "corsheaders",
    "storages",
    "django_rq",
    "authentication",
    "invitations",
    "lists",
    "notifications",
    "posts",
    "videos",
]

MIDDLEWARE = [
    "bugsnag.django.middleware.BugsnagMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hunchat.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "hunchat.wsgi.application"


CORS_ORIGIN_ALLOW_ALL = False
if os.environ.get("CORS_ORIGIN_ALLOW_ALL", "False") == "True":
    CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = json.loads(os.environ.get("CORS_ORIGIN_WHITELIST"))


# Django Rest Framework
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework_social_oauth2.authentication.SocialAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
    "SERIALIZER_EXTENSIONS": {
        "USE_HASH_IDS": True,
        "HASH_IDS_SOURCE": "authentication.HASH_IDS",
    },
}

HASHID_SALT = os.environ.get("HASHID_SALT")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=86400), # 60 days (change to 5 minutes)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("JWT",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))}

AUTH_USER_MODEL = "authentication.User"
AUTHENTICATION_BACKENDS = [
    # Apple OAuth2
    "social_core.backends.apple.AppleIdAuth",

    # django-rest-framework-social-oauth2
    "rest_framework_social_oauth2.backends.DjangoOAuth2",

    # Django
    "django.contrib.auth.backends.ModelBackend",
]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Apple configurations
# https://python-social-auth.readthedocs.io/en/latest/backends/apple.html

SOCIAL_AUTH_APPLE_ID_CLIENT = os.environ.get("SOCIAL_AUTH_APPLE_ID_CLIENT")
SOCIAL_AUTH_APPLE_ID_TEAM = os.environ.get("SOCIAL_AUTH_APPLE_ID_TEAM")
SOCIAL_AUTH_APPLE_ID_KEY = os.environ.get("SOCIAL_AUTH_APPLE_ID_KEY")
SOCIAL_AUTH_APPLE_ID_SECRET = os.environ.get("SOCIAL_AUTH_APPLE_ID_SECRET")
SOCIAL_AUTH_APPLE_ID_SCOPE = ["email", "name"]
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True


# Queues
# https://github.com/rq/django-rq

RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "PASSWORD": "some-password",
        "DEFAULT_TIMEOUT": 360,
    },
    "with-sentinel": {
        "SENTINELS": [("localhost", 26736), ("localhost", 26737)],
        "MASTER_NAME": "redismaster",
        "DB": 0,
        "PASSWORD": "secret",
        "SOCKET_TIMEOUT": None,
        "CONNECTION_KWARGS": {"socket_connect_timeout": 0.3},
    },
    "high": {
        "URL": os.getenv(
            "REDISTOGO_URL", "redis://localhost:6379/0"
        ),  # If you're on Heroku
        "DEFAULT_TIMEOUT": 500,
    },
    "low": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
    },
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Storage
# Amazon Web Services Sobo 3

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_S3_HOST = os.environ.get("AWS_S3_HOST", "s3.amazonaws.com")
AWS_S3_CUSTOM_DOMAIN = "%s.%s" % (AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATIC_DIR = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    STATIC_DIR,
]
AWS_STATIC_LOCATION = "static"
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)


# Media files (Images, Videos)
# https://docs.djangoproject.com/en/3.1/topics/files/

AWS_MEDIA_LOCATION = os.environ.get("AWS_MEDIA_LOCATION")
DEFAULT_FILE_STORAGE = "hunchat.storage.S3MediaStorage"
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)


# Email configurations
# https://docs.djangoproject.com/en/3.1/topics/email/

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
if os.environ.get("EMAIL_USE_TLS", "True") == "False":
    EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ.get("AWS_SES_SMTP_USER")
EMAIL_HOST_PASSWORD = os.environ.get("AWS_SES_SMTP_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


# Hunchat config

USER_USERNAME_MAX_LENGTH = int(os.environ.get("USER_USERNAME_MAX_LENGTH", "15"))
POST_DESCRIPTION_MAX_LENGTH = int(os.environ.get("POST_DESCRIPTION_MAX_LENGTH", "200"))
