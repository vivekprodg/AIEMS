"""
Django settings for AIEMS project.
Optimized for production, security, rate limiting, and dynamic CMS email dispatches.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# ENVIRONMENT & CORE SECURITY CONFIGURATION
# ==============================================================================
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DEVELOPMENT = config('DEVELOPMENT', default=False, cast=bool)
STATIC_FOLDER = config('STATIC', default='static')

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='127.0.0.1,localhost,api.aiems.edu.np',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

# ==============================================================================
# APPLICATION DEFINITION (REGISTERED 'training' APP)
# ==============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-Party Apps
    'rest_framework',
    'corsheaders',
    'nested_admin',
    
    # CMS / Business Core Apps
    'home',
    'about',
    'program',
    'training', # Registered Training Core App
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AIEMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'AIEMS.wsgi.application'

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
if DEVELOPMENT and not config('DB_NAME', default=None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
            'NAME': config('DB_NAME', default='aiems_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# ==============================================================================
# CACHING CONFIGURATION
# ==============================================================================
CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': config('CACHE_LOCATION', default='aiems-cache-store'),
    }
}

# ==============================================================================
# EMAIL DEFAULT BACKEND DECLARATION
# ==============================================================================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# ==============================================================================
# DJANGO REST FRAMEWORK (DRF) RATE-LIMITING & THROTTLING
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': config('THROTTLE_ANON_RATE', default='60/minute'),
        'user': config('THROTTLE_USER_RATE', default='1000/day'),
        'contact': config('THROTTLE_CONTACT_RATE', default='5/minute'),
        'apply': config('THROTTLE_APPLY_RATE', default='5/minute'),
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append(
        'rest_framework.renderers.BrowsableAPIRenderer'
    )

# ==============================================================================
# CORS & CSRF TRUSTED ORIGINS CONFIGURATIONS
# ==============================================================================
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS', 
    default='', 
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=DEBUG, cast=bool)
else:
    CORS_ALLOW_ALL_ORIGINS = False

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='', 
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

# ==============================================================================
# SECURITY HEADERS & REVERSE PROXY SSL
# ==============================================================================
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DEBUG and not DEVELOPMENT, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG and not DEVELOPMENT, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=not DEBUG and not DEVELOPMENT, cast=bool)

SECURE_CONTENT_TYPE_OPTIONS = True
X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')
SECURE_REFERRER_POLICY = config('SECURE_REFERRER_POLICY', default='strict-origin-when-cross-origin')

if not DEBUG and not DEVELOPMENT:
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# ==============================================================================
# INTERNATIONALIZATION & LOCALIZATION
# ==============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES ARCHITECTURE
# ==============================================================================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_URL = '/img/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB limit
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB limit

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'