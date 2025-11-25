import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------
# SECRET KEY & DEBUG
# ---------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-later")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Detect if running on Google Cloud
# The K_SERVICE environment variable is set automatically by Google Cloud Run.
if os.getenv("K_SERVICE"):
    USE_GCP = True
else:
    USE_GCP = os.getenv("USE_GCP", "False").lower() == "true"

if USE_GCP:
    DEBUG = False
    # This is safe because Cloud Run sets this header and it cannot be spoofed.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    
    # ALLOWED_HOSTS for Google Cloud Run
    # The K_SERVICE environment variable is the name of the Cloud Run service.
    # The K_REVISION environment variable is the specific version of the service.
    # We can construct the URL from these.
    ALLOWED_HOSTS = [
        "lms-backend-536444006215.africa-south1.run.app",
    ]
    
    # CSRF_TRUSTED_ORIGINS for security
    CSRF_TRUSTED_ORIGINS = [
        "https://lms-backend-536444006215.africa-south1.run.app",
    ]
    # Add the service URL to CSRF_TRUSTED_ORIGINS
    if service_url := os.getenv("K_SERVICE"):
        # The default URL for a Cloud Run service is https://<service-name>-<project-hash>-<region>.a.run.app
        # We can get the project hash and region from the metadata server, but for simplicity,
        # we will use the known URL.
        CSRF_TRUSTED_ORIGINS.append(f"https://{service_url}")

    # Database settings for GCP
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": f"/cloudsql/{os.getenv('DB_CONNECTION_NAME')}",
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "NAME": os.getenv("DB_NAME"),
        }
    }
elif os.getenv("RENDER"):
    # Production on Render: use PostgreSQL
    ALLOWED_HOSTS = []
    if RENDER_EXTERNAL_HOSTNAME := os.getenv("RENDER_EXTERNAL_HOSTNAME"):
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
        
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }
elif os.getenv('DB_HOST'):
    # Local development with Cloud SQL Proxy
    ALLOWED_HOSTS = ["*"]
    DATABASES = {
        'default': dj_database_url.config(
            default=f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
            conn_max_age=600
        )
    }
else:
    # local: fallback to SQLite
    ALLOWED_HOSTS = ["*"]
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
    "drf_yasg",
    "rest_framework_simplejwt",
    "storages", # For Google Cloud Storage

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
    "https://ccgd-learn-central.vercel.app",
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

# ---------------------------------------
# GOOGLE CLOUD STORAGE
# ---------------------------------------
if USE_GCP:
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")
    MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"
