"""
Django settings for omcen project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(Path(BASE_DIR, '.env'))

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'social_django',
    'omcen',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': env.db(),
}

AUTH_USER_MODEL = 'omcen.OmcenUser'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'css'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login??????
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# ???????????????????????????
LOGIN_REDIRECT_URL = '/mypage/'
# ??????????????????????????????
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

# ??????????????????
EMAIL_HOST = env('EMAIL_HOST')
# ?????????
EMAIL_PORT = env('EMAIL_PORT', int)
# ?????????
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
# ???????????????
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# ???????????????????????????
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# ????????????????????????????????????
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ?????????????????????????????????
ACCOUNT_UNIQUE_EMAIL = True
# ???????????????????????????????????????????????????
ACCOUNT_EMAIL_REQUIRED = True
# ?????????????????????
EMAIL_USE_TLS = True
# ??????????????????????????????[??????]
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# ??????????????????????????????????????????
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

# ?????????????????????????????????????????????????????????????????????????????????
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ??????????????????????????????????????????????????????
ACCOUNT_USERNAME_REQUIRED = True
# ????????????????????????????????????????????????????????????????????????
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
# ??????????????????????????????????????????????????????????????????
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# ????????????????????????
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ??????????????????????????????????????????[???]
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600
# ????????????????????????????????????????????????????????????????????????URL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL

# ???????????????MIME??????????????????????????????
SECURE_CONTENT_TYPE_NOSNIFF = True

# ??????????????????????????????
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
        ],
    },
}

SITE_ID = 1
