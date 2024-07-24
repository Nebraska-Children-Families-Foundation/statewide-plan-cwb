from pathlib import Path
from decouple import config
from django.contrib.messages import constants as messages
import mimetypes

mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# General Configuration
SECRET_KEY = config('SECRET_KEY')
ENVIRONMENT = config('DJANGO_ENV')

# Development settings
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    CSRF_COOKIE_SECURE = False

# Production settings
elif ENVIRONMENT == 'production':
    DEBUG = False
    ALLOWED_HOSTS = ['statewideplan.bringupnebraska.org']
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_DOMAIN = '.bringupnebraska.org'
    CSRF_TRUSTED_ORIGINS = ['https://statewideplan.bringupnebraska.org']

# Test server settings
elif ENVIRONMENT == 'test':
    DEBUG = True
    ALLOWED_HOSTS = ['statewideplan.ncffapps.dev']
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_DOMAIN = 'statewideplan.ncffapps.dev'
    CSRF_TRUSTED_ORIGINS = ['https://statewideplan.ncffapps.dev']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'smart_selects',
    'widget_tweaks',
    'core',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'users.middleware.CheckPasswordResetMiddleware',
]

ROOT_URLCONF = 'statewideplanCWB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'statewideplanCWB.wsgi.application'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Database Configuration
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('PROD_DATABASE_NAME'),
            'USER': config('PROD_DATABASE_USER'),
            'PASSWORD': config('PROD_DATABASE_PASSWORD'),
            'HOST': config('PROD_DATABASE_HOST'),
            'PORT': config('PROD_DATABASE_PORT'),
        }
    }
elif ENVIRONMENT == 'test':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('TEST_DATABASE_NAME', default='test_db'),
            'USER': config('TEST_DATABASE_USER', default='test_user'),
            'PASSWORD': config('TEST_DATABASE_PASSWORD', default='test_password'),
            'HOST': config('TEST_DATABASE_HOST', default='localhost'),
            'PORT': config('TEST_DATABASE_PORT', default='5432'),
        }
    }
elif ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR / 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
AUTH_USER_MODEL = 'users.AppUser'

# Login URL
LOGIN_URL = 'users:login'

# Login Redirection
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
