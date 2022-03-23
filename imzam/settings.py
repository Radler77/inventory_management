"""
Django settings for imzam project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from distutils.util import strtobool
from pathlib import Path
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "data", "static")
STATIC_URL = "static/"
# Media files (e.g., uploads by users)
MEDIA_ROOT = os.path.join(BASE_DIR, "data", "media")
MEDIA_URL = "media/"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# For production, overwrite in local_settings.py
# generate using this code:
# import random, string
# "".join(random.choices([c for c in string.printable if c not in "\t\n\r\x0b\x0c], k=64))
SECRET_KEY = os.getenv("SECRET_KEY", None)

# For deployment, set to False in local_settings.py
DEBUG = bool(strtobool(os.getenv("DEBUG", "false")))

DEFAULT_DOMAIN = "https://inv.zam.haus"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-ALLOWED_HOSTS
allowed_hosts = os.getenv("ALLOWED_HOSTS", ".localhost,127.0.0.1,[::1]")
ALLOWED_HOSTS = list(map(str.strip, allowed_hosts.split(",")))

# Application definition

INSTALLED_APPS = [
    "inventory.apps.InventoryConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "mozilla_django_oidc",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_bootstrap5",
    "extra_views",
    "computedfields",
    "accounts",
    "django_bootstrap_icons",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

COMPUTEDFIELDS_ALLOW_RECURSION = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'mozilla_django_oidc.middleware.SessionRefresh',
    'imzam.zam_local.ZAMLocalMiddleware',
]

ROOT_URLCONF = "imzam.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "imzam.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django"),
        "USER": os.getenv("POSTGRES_USER", "django"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}


# ================================================================
# OpenID and Athentication Configuration
# ================================================================

AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.auth.CustomOidcAuthenticationBackend',
)

OIDC_RP_CLIENT_ID = os.getenv('OIDC_RP_CLIENT_ID', 'inv.zam.haus')
OIDC_RP_CLIENT_SECRET = os.getenv('OIDC_RP_CLIENT_SECRET')
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv(
    'OIDC_OP_AUTHORIZATION_ENDPOINT',
    'https://login.zam.haus/auth/realms/ZAM/protocol/openid-connect/auth')
OIDC_OP_TOKEN_ENDPOINT = os.getenv(
    'OIDC_OP_TOKEN_ENDPOINT',
    'https://login.zam.haus/auth/realms/ZAM/protocol/openid-connect/token')
OIDC_OP_USER_ENDPOINT = os.getenv(
    'OIDC_OP_USER_ENDPOINT',
    'https://login.zam.haus/auth/realms/ZAM/protocol/openid-connect/userinfo')
OIDC_OP_LOGOUT_URL = os.getenv(
    'OIDC_OP_LOGOUT_URL',
    'https://login.zam.haus/auth/realms/ZAM/protocol/openid-connect/logout?redirect_uri={}')
if OIDC_OP_LOGOUT_URL:
    OIDC_OP_LOGOUT_URL_METHOD = 'accounts.auth.provider_logout'
OIDC_RP_SIGN_ALGO = 'RS256'
OIDC_OP_JWKS_ENDPOINT = os.getenv(
    'OIDC_OP_JWKS_ENDPOINT',
    'https://login.zam.haus/auth/realms/ZAM/protocol/openid-connect/certs')
LOGIN_REDIRECT_URL = '/'
ALLOW_LOGOUT_GET_METHOD = True
LOGOUT_REDIRECT_URL = '/'
OIDC_CLAIM_REFERENCE_KEY = os.getenv("OIDC_CLAIM_REFERENCE_KEY", 'ldap_id')
OIDC_CLAIM_USERNAME_KEY = os.getenv("OIDC_CLAIM_USERNAME_KEY", 'preferred_username')
LOGIN_URL = '/oidc/authenticate'

OIDC_ADMIN_GROUPS = list(map(
    str.strip,
    os.getenv("OIDC_ADMIN_GROUPS", 'Admin, InventoryAdmin').split(',')))

OIDC_STAFF_GROUPS = list(map(
    str.strip,
    os.getenv("OIDC_ADMIN_GROUPS", 'Admin, InventoryAdmin').split(',')))

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "de-DE"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True


LANGUAGES = [
    ("en", "English"),
    ("de", "German"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ================================================================
# MQTT Configuration
# ================================================================

# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#connect-reconnect-disconnect
MQTT_CLIENT_KWARGS = dict(
    client_id=os.getenv("MQTT_CLIENT_ID", "imzam"),
    transport=os.getenv("MQTT_TRANSPORT", "websockets"))
MQTT_SERVER_KWARGS = dict(
    host=os.getenv("MQTT_SERVER_HOSTNAME", "mqtt.zam.haus"),
    port=int(os.getenv("MQTT_SERVER_PORT", "443")),
    keepalive=120)
MQTT_SERVER_SSL=strtobool(os.getenv("MQTT_SERVER_SSL", "true"))
MQTT_PASSWORD_AUTH = dict(
    username=os.getenv("MQTT_USERNAME", "im.zam.haus-django"),
    password=os.getenv("MQTT_PASSWORD", ""))
# this topic is write-restricted on mqtt.zam.haus
MQTT_PRINTER_TOPIC = "im-label-print-queue/"

MQTT_ZAMIP_SERVER_KWARGS = dict(
    host=os.getenv("MQTT_ZAMIP_SERVER_HOSTNAME", "mqtt.sesam.zam.haus"),
    port=int(os.getenv("MQTT_ZAMIP_SERVER_PORT", "443")),
    keepalive=120)
MQTT_ZAMIP_SERVER_SSL=strtobool(os.getenv("MQTT_SERVER_SSL", "true"))
MQTT_ZAMIP_PASSWORD_AUTH = dict(
    username=os.getenv("MQTT_ZAMIP_USERNAME", "inv.zam.haus-django"),
    password=os.getenv("MQTT_ZAMIP_PASSWORD", ""))


# Overwrite default settings with local_settings.py configuration
if not os.getenv("IGNORE_LOCAL_SETTINGS", False):
    try:
        from .local_settings import *
    except ImportError:
        pass


# ================================================================
# Client IP Detection Using ipware
# ================================================================

#PROXY_HOSTNAME = "nginx"
#try:
#    _, _, _nginx_address = socket.gethostbyname_ex(PROXY_HOSTNAME)
#except socket.gaierror:
#    _nginx_address = None
#
#if _nginx_address:
#    IPWARE_REVERSE_PROXIES = [
#        ReverseProxy(Header("X-Forwarded-For"), *_nginx_address),
#    ]
#else:
#    IPWARE_REVERSE_PROXIES = []


# ================================================================
# Logging
# ================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'WARNING'
        },
    },
}
