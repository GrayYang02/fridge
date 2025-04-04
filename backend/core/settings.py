from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key'

DEBUG = True


ALLOWED_HOSTS = ["127.0.0.1", "localhost","3.139.71.177"]
SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),

}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),

}


INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
]
AUTH_USER_MODEL = 'core.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'fridgeserver.urls'


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

WSGI_APPLICATION = 'fridgeserver.wsgi.application'





if 'test' in sys.argv or  os.getenv('DJANGO_ENV') == 'test':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'django_db',
    #         'USER': 'django_user',
    #         'PASSWORD': 'wb4697',
    #         'HOST': 'database-1.czm20ai6yn1e.us-east-2.rds.amazonaws.com',
    #         'PORT': '3306',
    #         'OPTIONS': {
    #             'auth_plugin': 'caching_sha2_password',
    #         },
    #     }
    # }
    # todo for github testing
      DATABASES = {
        'default': {

            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("DB_NAME"),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST"),
            'PORT': os.getenv("DB_PORT"),
            # 'OPTIONS': {
            #     'auth_plugin': 'caching_sha2_password',
            # },

            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': BASE_DIR / 'db.sqlite3',

        }
    }


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True



### Media - profile pics
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

### API parts
API_KEY = os.getenv("API_KEY")
APP_ID = os.getenv("APP_ID")

print("Using DB:", DATABASES['default'])

print("📦 DB in use:", os.getenv('DB_NAME'))
print("django env:", os.getenv('DJANGO_ENV'))

### API parts
API_KEY = "sk-94945667a547494a9adeefcff1d5a3a1"
RECIPE_APP_ID = 'a78c9f45e02c411da89cd9c95a1b86aa'
SUGGEST_APP_ID = '1fdcf8a05beb4c2b960cb6673c9e5e70'

