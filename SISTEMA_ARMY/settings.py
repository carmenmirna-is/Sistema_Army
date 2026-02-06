"""
Django settings for _army_ project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-h#i1o=a$xmq#j7yjqeb6k=*2y!0edy40r7(_rn6pn&t!od1ai(')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Configuración para producción
if os.environ.get('RENDER'):
    ALLOWED_HOSTS = ['.onrender.com']
elif os.environ.get('RAILWAY_ENVIRONMENT_NAME') or os.environ.get('RAILWAY_ENVIRONMENT'):
    ALLOWED_HOSTS = [
        '.railway.app', 
        '.up.railway.app',
        'sistema-army-production.up.railway.app'  # Pon tu dominio específico aquí
    ]
else:
    ALLOWED_HOSTS = ['*']

# CSRF para Railway
if os.environ.get('RAILWAY_ENVIRONMENT_NAME') or os.environ.get('RAILWAY_ENVIRONMENT'):
    CSRF_TRUSTED_ORIGINS = [
        'https://*.railway.app',
        'https://*.up.railway.app',
        'https://sistema-army-production.up.railway.app'  # Tu dominio específico
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # ← Agregar ANTES de 'cloudinary'
    'cloudinary', 
    'army',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SISTEMA_ARMY.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SISTEMA_ARMY.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

if os.environ.get('DATABASE_URL'):
    # Producción - PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Desarrollo - SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'es-bo'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise para servir archivos estáticos en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# LOGIN URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'directorio_army'
LOGOUT_REDIRECT_URL = 'login'

# Configuración de mensajes
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

import cloudinary

# Configuración de Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

# Cambiar el almacenamiento por defecto
if os.environ.get('RAILWAY_ENVIRONMENT_NAME') or os.environ.get('RAILWAY_ENVIRONMENT'):
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'