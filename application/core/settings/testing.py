from core.settings.base import *

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# CELERY_TASK_EAGER_PROPAGATES = True
# CELERY_TASK_ALWAYS_EAGER = True
BROKER_BACKEND = "memory://"
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "db+sqlite:///results.sqlite"
