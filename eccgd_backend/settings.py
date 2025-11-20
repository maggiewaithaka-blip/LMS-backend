import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# SECRET KEY & DEBUG
# ---------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-later")

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host] or ["*"]

# ---------------------------------------
# INSTALLED APPS
# ---------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd Party Apps
    "rest_framework",
    "corsheaders",
    "django_celery_beat",
    "drf_yasg",
    "rest_framework_simplejwt",

    # Project apps
    'users',
    'courses',
    'enrollment',
    'assignments',
    'quizzes',
    'grades',
    'messaging',
    'storage',
    'reports',
    'plugins',
]

# ---------------------------------------
# MIDDLEWARE
# ---------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # required on Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",       # only if using CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------
# TEMPLATES
# ---------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------
# URLS & WSGI
# ---------------------------------------
ROOT_URLCONF = "eccgd_backend.urls"

WSGI_APPLICATION = "eccgd_backend.wsgi.application"

# ---------------------------------------
# DATABASES
# ---------------------------------------
# Render sets an environment variable: RENDER = "true"
IS_RENDER = os.getenv("RENDER")

if IS_RENDER:
    # production: use PostgreSQL
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # local: fallback to SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------
# STATIC & MEDIA FILES
# ---------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------
# CORS (Enable only if needed)
# ---------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------------------
# AUTHENTICATION
# ---------------------------------------
AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

# ---------------------------------------
# DEFAULT AUTO FIELD
# ---------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
