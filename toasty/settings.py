import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes")

# Secret key - use environment variable in production
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "unsafe-dev-secret-key-do-not-use-in-production"
    else:
        raise ValueError("SECRET_KEY environment variable must be set in production")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") if os.environ.get("ALLOWED_HOSTS") else []

# GitHub AIBot Configuration
GITHUB_AIBOT_APP_NAME = os.environ.get("GITHUB_AIBOT_APP_NAME")
GITHUB_AIBOT_APP_ID = os.environ.get("GITHUB_AIBOT_APP_ID")
GITHUB_AIBOT_PRIVATE_KEY_B64 = os.environ.get("GITHUB_AIBOT_PRIVATE_KEY_B64")
GITHUB_AIBOT_WEBHOOK_SECRET = os.environ.get("GITHUB_AIBOT_WEBHOOK_SECRET")

# Gemini AI Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "blank")
GEMINI_GENERATION_MODEL = os.environ.get("GEMINI_GENERATION_MODEL")
GEMINI_EMBEDDING_MODEL = os.environ.get("GEMINI_EMBEDDING_MODEL")

# Celery Configuration
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Qdrant Vector DB Configuration
QDRANT_HOST = os.environ.get("QDRANT_HOST", "qdrant")
QDRANT_VECTOR_SIZE = int(os.environ.get("QDRANT_VECTOR_SIZE", "768"))
QDRANT_HTTP_PORT = int(os.environ.get("QDRANT_HTTP_PORT", "6333"))


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "toasty.aibot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "toasty.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "toasty.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Use PostgreSQL when DATABASE_URL is configured, otherwise SQLite for development

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL configuration for Docker/production
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "toasty"),
            "USER": os.environ.get("POSTGRES_USER", "toasty"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    # SQLite configuration for local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redis Cache Configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://redis:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}
