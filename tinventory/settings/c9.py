from .base_settings import *
import os

# ENVIRONMENT VARIABLES: DJANGO_SETTINGS_MODULE, SECRET_KEY, DB_USER. DB_PASSWORD, DB_NAME, EMAIL_PASSWORD

# SECURITY STUFF
DEBUG = True

# SITE-SPECIFIC INSTALLATION

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
    ]

# DATABASE SETTINGS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
}

# LOCAL STUFF
INTERNAL_IPS = ('127.0.0.1','0.0.0.0:8080')
ALLOWED_HOSTS = ['tinventory4-pkugelmass.c9users.io',]

# SPECIAL APPS

def show_toolbar(request):
    return True
    
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_COLLAPSED" : True,
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

DEFAULT_FROM_EMAIL = '<C9 T-Repo> tinventory900@gmail.com'