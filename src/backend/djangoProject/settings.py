"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os.path
import json
from .vault_config import get_db_credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vfvsk%cx11j^o)to!8om3mt^tf72j81h3dlp&d_%)8-8e=-q-g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'API.apps.ApiConfig',
    'authentication.apps.AuthenticationConfig',
    'game.apps.GameConfig',
    'django_extensions',
    'user.apps.UserConfig',
    'friends.apps.FriendsConfig',
    'tournaments.apps.TournamentsConfig',
    'dashboard.apps.DashboardConfig',
    'matchMaking',
    'rest_framework',
    'asgiref',
    'rest_framework_simplejwt.token_blacklist',
    # 2FA
    'django_otp',
    # 'two_factor.plugins.phonenumber',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'qr_code',
    'channels',
    'django_countries',
    'two_factor',
    # JWT
    'rest_framework_simplejwt',
]

ASGI_APPLICATION = 'djangoProject.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        }
    }
}

LOGIN_URL = 'authentication:login'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    "authentication.middleware.AttachResponseMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TWO_FACTOR_PATCH_ADMIN = True
TWO_FACTOR_CALL_GATEWAY = None
TWO_FACTOR_SMS_GATEWAY = None

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'djangoProject', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# db_credentials = get_db_credentials()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "USER": "postgres",
        "PASSWORD": "1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}


# JWT

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
       'authentication.authentication.CookieJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}


SESSION_COOKIE_SECURE = False  # Use True for production with HTTPS
CSRF_COOKIE_SECURE = False     # Use True for production with HTTPS
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

#PASSWORD HASHING

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Luxembourg'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "djangoProject/static")]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TWO_FACTOR_SETUP_REDIRECT_URL = 'home'
LOGIN_URL = 'two_factor:login'  # 2FA login view
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Blockchain settings
# note: do not forget to change contract address when new deploy
# note : do not forget to change the provider URI when deploying on a new network
#WEB3_PROVIDER_URI = 'https://eth-sepolia.g.alchemy.com/v2/vJ9BDo8uiTvIVlOhxJhcfXahMs4oSBMJ'
WEB3_PROVIDER_URI = 'http://127.0.0.1:8545'
CONTRACT_ADDRESS = '0x68a14A854C7397811b4c5FB5D83889a7874C817D'
ABI_FILE_PATH = os.path.join(BASE_DIR, 'blockchain', 'ScoreContract.json')
ETHERSCAN_BASE_URL = 'https://sepolia.etherscan.io/tx'

with open(ABI_FILE_PATH, 'r') as abi_file:
    contract_data = json.load(abi_file)
    CONTRACT_ABI = contract_data['abi']
