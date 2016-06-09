"""
Django settings for django_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h3zJK5zICr08XXaFQVOPqO8U56Yz9IhfK4BOmZBxOq2NgQdBzx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['red-diesel.ru', 'www.red-diesel.ru']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'tinymce',
    'rd'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = [
    # 'django.template.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
]

ROOT_URLCONF = 'django_project.urls'

WSGI_APPLICATION = 'django_project.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'django_project/templates/'),]
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'django_project/static/'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'django_project/static_root/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'django_project/static/uploads/')
MEDIA_URL = '/static/uploads/'


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = ''
EMAIL_HOST_USER ='robot@red-diesel.ru'
EMAIL_HOST_PASSWORD = 'robotchappie'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVER_EMAIL = 'robot@red-diesel.ru'
ADMINS = (
    ('g10k', 'g10k.info@gmail.com'),
    ('daron', 'info@red-diesel.ru'),
)


TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}