from .common import *


SECRET_KEY = 'django-insecure-d4qz027gaa6c^k%s(p_)__tusr6*r4g@g(iyl+q2yc-9m*u-dk'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront3',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Pokemony',
    }
}
