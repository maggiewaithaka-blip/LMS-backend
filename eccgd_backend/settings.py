# ---------------------------------------
# CKEDITOR CONFIG
# ---------------------------------------
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}
from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# SECRET KEY & DEBUG
# ---------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY environment variable must be set in production!")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# Environment-based database and host config
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    ALLOWED_HOSTS = ["lms.careerguidancecollege.com"]
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=False  # Fly.io Postgres does not require ssl by default
        )
    }
else:
    # fallback to SQLite
    ALLOWED_HOSTS = ["lms.careerguidancecollege.com"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

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
    "nested_admin",
    "drf_yasg",
    "rest_framework_simplejwt",
    "ckeditor",

    # Project apps
    'users',
    'courses',
    'enrollment',
    'storage',
    'reports',
    # "storages", # For Google Cloud Storage (removed for Fly.io)
    ]

# ---------------------------------------
# AUTHENTICATION
# ---------------------------------------
AUTH_USER_MODEL = "users.User"

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
# This section is now handled above, so it is removed from here.

# ---------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ---------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------------------------
# STATIC FILES
# ---------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ---------------------------------------
# MEDIA FILES
# ---------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# ---------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------
# CORS
# ---------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://lms.careerguidancecollege.com",
]
CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------
# DRF
# ---------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ---------------------------------------
# CELERY
# ---------------------------------------
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379")
CELERY_TIMEZONE = "UTC"

# ---------------------------------------
# LOGGING
# ---------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
        "eccgd_backend": {
            "handlers": ["console"],
            "level": os.getenv("ECCGD_LOG_LEVEL", "DEBUG"),
        },
    },
}

# ---------------------------------------
# SWAGGER & REDOC
# ---------------------------------------
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "JSON_EDITOR": True,
}

REDOC_SETTINGS = {
    "LAZY_RENDERING": True,
}

CSRF_TRUSTED_ORIGINS = [
    "https://lms-backend-qhvvka.fly.dev",
    # add other trusted origins if needed
]


