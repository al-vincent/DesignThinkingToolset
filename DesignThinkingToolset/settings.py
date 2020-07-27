"""
Django settings for DesignThinkingToolset project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')  # html templates
STATIC_DIR = os.path.join(BASE_DIR, 'static')       # js, css, imgs etc.
MEDIA_DIR = os.path.join(BASE_DIR, 'media')         # media files


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'PostItFinder',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DesignThinkingToolset.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'DesignThinkingToolset.wsgi.application'

# Sessions
# https://docs.djangoproject.com/en/3.0/topics/http/sessions/ 

# Set session info to write to file, instead of db
SESSION_ENGINE = 'django.contrib.sessions.backends.file' 
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
IMAGE_KEY = "image_info"
REGION_KEY = "regions"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR, ]

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

if 'DJANGO_DEBUG_FALSE' in os.environ:  
    DEBUG = False
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  
    ALLOWED_HOSTS = [os.environ['SITENAME']]  
    STATIC = STATIC_ROOT
else:
    DEBUG = True  
    SECRET_KEY = 'insecure-key-for-dev'
    ALLOWED_HOSTS = []
    STATIC = STATIC_DIR

# Override the default max data upload value

DATA_UPLOAD_MAX_MEMORY_SIZE = 4194304

# Azure settings - Custom Vision Object Detection

OBJ_DET_PREDICTION_KEY = os.environ['SNIP_OBJ_DET_PRED_KEY']
OBJ_DET_PROJECT_ID = os.environ['SNIP_OBJ_DET_PROJ_ID']
OBJ_DET_PUBLISHED_NAME = os.environ['SNIP_OBJ_DET_PUB_NAME']
OBJ_DET_BASE_URL = 'snip-object-detection.cognitiveservices.azure.com'
OBJ_DET_API_URL = f'/customvision/v3.0/Prediction/{OBJ_DET_PROJECT_ID}/detect/iterations/{OBJ_DET_PUBLISHED_NAME}/image'
OK_IMAGE_TYPES = ['jpeg', 'bmp', 'png', 'gif']

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': ' {levelname} {name} {funcName} {message}',
            'style': '{'
        },
        'file': {
            'format': '{asctime} {name} {levelname} {message}',
            'style': '{'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'snip_debug.log'),
            'maxBytes': 1024*1024*20, # Logfile size: 20MB
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }
}