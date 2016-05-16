"""
Django settings for solo project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)


STRIPE_API_KEY = 'sk_test_1AFSPD5Dg8RihyPPtylWiSsR'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '))*bdzp8!4)acc45^ms4(srw%nh8^yt+_55775y&9zt%i3rx_i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

MEDIA_URL = STATIC_URL + "media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
	'django.contrib.sites',
	
    'seller',
	
	# stripe authentication through allauth
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.stripe',

]

# add login redirect
LOGIN_REDIRECT_URL = '/new'


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'solo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
				
            ],
        },
    },
]

WSGI_APPLICATION = 'solo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'solo',
        'USER': 'postgres',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/


## stripe allauth and socialauth
SITE_ID = 1

#################################################################
# allauth settings for social connections

# source: https://realpython.com/blog/python/adding-social-authentication-to-django/
AUTHENTICATION_BACKENDS = (
	#'social.backends.google.GoogleOAuth',
	#'social.backends.google.GoogleOAuth2',
	#'social.backends.instagram.InstagramOAuth2',
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
)


# dictionary containing provider specific settings.
SOCIALACCOUNT_PROVIDERS = {
	'stripe':
		{'SCOPE': ['read_write',],
		}
}

# attempt to bypass the signup form by using fields (e.g. username, email) 
# retrieved from the social account provider. If a conflict arises due to a 
# duplicated e-mail the signup form will still kick in
SOCIALACCOUNT_AUTO_SIGNUP = True

#enforce uniqueness of e-mail address
ACCOUNT_UNIQUE_EMAIL = True

# user is required ot enter a username when signing up. note that the
# user will be asked to do so even if ACCOUNT_AUTHENTICATION_METHOD is set 
# to email. Set to False when you do not wish to prompt the user to enter a username.
ACCOUNT_USERNAME_REQUIRED = False

# the use is required to hand over an e-mail address when signing up
ACCOUNT_EMAIL_REQUIRED = True

# request email address from third part account provider
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED




