"""
Django settings for jobya project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cba46po#-5(@r^enof&%+j=!9dd9=&iq3o6e7ce(blw6se(#u6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mysite.com', 'localhost',
                 '127.0.0.1']  # I used this for testing


# Application definition

INSTALLED_APPS = [
    'chat',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'job.apps.JobConfig',
    'user.apps.UserConfig',
    'blog',
    'crispy_forms',
    'payment',
    'social_django',  # social-auth-app-django
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

ROOT_URLCONF = 'jobya.urls'

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

WSGI_APPLICATION = 'jobya.wsgi.application'
ASGI_APPLICATION = 'jobya.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # 'CONFIG': {
        #     'hosts': [('127.0.0.1', 6379)],
        # }
    }
}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRSIPY_TEMPLATE_PACK = 'bootstrap5'

LOGIN_REDIRECT_URL = 'job-home'

LOGIN_URL = 'login'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')   

STRIPE_PUBLIC_KEY = 'pk_test_51LzOeaGSSxV2P1yNR6uNxfXPdsATOXGxNtB5xv8ox5Wal7O5MESopp9potueteddlbp7MGjh9Jj7f6xr3ggwkT6P00MAKaSOmy'

STRIPE_SECRET_KEY = 'sk_test_51LzOeaGSSxV2P1yNden2ofolaLXH1BtFqUIv5akUVRAiq4Ph8q4eiR5QA9plbi3K7LXd5PRDkaw62qU2exSPrcD500oJOMy5Ng'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
]

# OAUTH AUTHENTICATION CREDENTIALS
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
#SOCIAL_AUTH_FACEBOOK_SCOPE = ['']

SOCIAL_AUTH_TWITTER_KEY = ''
SOCIAL_AUTH_TWITTER_SECRET = ''

# replace with yours
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '946875859866-q27u3q0u20gar2fh5r6lsnajq2v9udua.apps.googleusercontent.com'
# replace with yours
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# Coinbase crypto payment 
# Please set up account on coinbase-commerce to fill this infos
COINBASE_COMMERCE_API_KEY = 'e3ed9dd2-7e9d-4e62-9533-4d0195a5a2f9'
COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET = ''
