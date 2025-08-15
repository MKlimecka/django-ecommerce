from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = []

# Database
# Update these settings with your local database credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-db-name',
        'HOST': 'localhost',
        'USER': 'your-db-username',
        'PASSWORD': 'your-db-password',
    }}