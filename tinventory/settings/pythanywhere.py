from .base_settings import *
import os

# What needs to be set in env variables?
# --SECRET_KEY
# --DJANGO_SETTINGS_MODULE
# --DB_NAME
# --DB_USER
# --DB_PASSWORD
# --EMAIL_PASSWORD

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pktcsb$tcsb',
        'USER': 'pktcsb',
        'PASSWORD': 'what3v3r',
        'HOST': 'pktcsb.mysql.pythonanywhere-services.com',
    
    },
}

ALLOWED_HOSTS = ['pktcsb.pythonanywhere.com',]

DEFAULT_FROM_EMAIL = '<PythAny T-Repo> tinventory900@gmail.com'