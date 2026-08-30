from .base import *
from decouple import config


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",  # or the frontend URL
#     "http://127.0.0.1:5500",  # or the frontend URL
# ]