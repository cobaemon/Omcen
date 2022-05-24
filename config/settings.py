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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# キーフォルダの場所
KEYS_DIR = Path(BASE_DIR, 'keys')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['omcen.org']
CSRF_TRUSTED_ORIGINS = ['https://omcen.org']

# Application definition

INSTALLED_APPS = [
    'accounts',
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
    'password_box',
    'file_encryption',
    'tango',
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
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'ATOMIC_REQUESTS': True,
    }
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
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static', 'css'),
    os.path.join(BASE_DIR, 'static', 'js'),
    os.path.join(BASE_DIR, 'static', 'img'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login設定
AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# ログイン後の移動先
LOGIN_REDIRECT_URL = '/omcen/my_page'
# ログアウト後の移動先
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'

# カスタムアカウント
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'omcen.OmcenUser.username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# メールホスト
EMAIL_HOST = os.environ.get('EMAIL_HOST')
# ポート
EMAIL_PORT = os.environ.get('EMAIL_PORT', int)
# 送信元
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
# パスワード
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# メールを実際に送る
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# メールアドレスの検証方法
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# メールをユニークにする
ACCOUNT_UNIQUE_EMAIL = True
# メールアドレスの入力を必須にするか
ACCOUNT_EMAIL_REQUIRED = True
# メールの暗号化
EMAIL_USE_TLS = True
# 確認メールの有効期限[日数]
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
# 確認メールに特定キーを入れる
ACCOUNT_EMAIL_CONFIRMATION_HMAC = True

# サインインにユーザー名かメールアドレス又は両方を使うか
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# サインアップ時にユーザ名を入力させる
ACCOUNT_USERNAME_REQUIRED = True
# サインアップ時にメールアドレスを２回入力させるか
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
# サインアップ時にパスワードを２回入力させるか
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
# ログイン試行回数
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# ログイン失敗時のクールダウン[秒]
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 600
# 電子メールの認証が成功した後にリダイレクトされるURL
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_REDIRECT_URL

# ブラウザのMIMEタイプを自動判別する
SECURE_CONTENT_TYPE_NOSNIFF = True

# ソーシャルアカウント
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
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

SITE_ID = 2
