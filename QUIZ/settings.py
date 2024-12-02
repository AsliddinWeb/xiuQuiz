import os
from pathlib import Path

# Loyiha asosiy katalogi
BASE_DIR = Path(__file__).resolve().parent.parent

# Maxfiy kalit (dev uchun yaratilgan)
SECRET_KEY = 'django-insecure-your-secret-key'

# Debug holati (ishlab chiqishda `True`, ishlab chiqarishda `False`)
DEBUG = True

ALLOWED_HOSTS = []

# O'rnatilgan dasturlar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Global APPS
    'import_export',

    # Local APPS
    'student_app',  # Talabalar uchun ilova
    'quiz_app',     # Quiz uchun ilova
]

# Middleware (oraliq qatlamlar)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL konfiguratsiya
ROOT_URLCONF = 'QUIZ.urls'

# Shablonlar sozlamalari
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Shablonlar katalogi
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

# WSGI dastur
WSGI_APPLICATION = 'QUIZ.wsgi.application'

# Ma'lumotlar bazasi
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite ma'lumotlar bazasi
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Auth foydalanuvchi paroli uchun sozlamalar
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

# Til va vaqt zonasi
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Statik fayllar uchun sozlamalar
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Statik fayllar katalogi

# Media fayllar uchun sozlamalar
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Yuklangan fayllar katalogi

# Default avtentifikatsiya modeli
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
