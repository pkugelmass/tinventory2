from .base_settings import *
import os

# ENVIRONMENT VARIABLES: DJANGO_SETTINGS_MODULE, SECRET_KEY, DB_USER. DB_PASSWORD, DB_NAME, DB_HOST, EMAIL_PASSWORD, APP_INSIGHTS_KEY

# SECURITY STUFF
DEBUG = True

# SITE-SPECIFIC INSTALLATION

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
    'applicationinsights',
    ]
    
MIDDLEWARE = MIDDLEWARE + [
    'applicationinsights.django.ApplicationInsightsMiddleware',
    ]
    
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    },
}

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "tinventory900@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# APPLICATION INSIGHTS
APPLICATION_INSIGHTS = {
    # (required) Your Application Insights instrumentation key
    'ikey': os.environ.get('APP_INSIGHTS_KEY'),
    
    # (optional) By default, request names are logged as the request method
    # and relative path of the URL.  To log the fully-qualified view names
    # instead, set this to True.  Defaults to False.
    'use_view_name': True,
    
    # (optional) To log arguments passed into the views as custom properties,
    # set this to True.  Defaults to False.
    'record_view_arguments': True,
    
    # (optional) Exceptions are logged by default, to disable, set this to False.
    'log_exceptions': False,
    
    # (optional) Events are submitted to Application Insights asynchronously.
    # send_interval specifies how often the queue is checked for items to submit.
    # send_time specifies how long the sender waits for new input before recycling
    # the background thread.
    'send_interval': 1.0, # Check every second
    'send_time': 3.0, # Wait up to 3 seconds for an event
    
    # (optional, uncommon) If you must send to an endpoint other than the
    # default endpoint, specify it here:
    'endpoint': "https://dc.services.visualstudio.com/v2/track",
}

# DJANGO-DEBUG-TOOLBAR

def show_toolbar(request):
    return True
    
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_COLLAPSED" : True,
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

# EMAIL
DEFAULT_FROM_EMAIL = '<T-Repo Azure Staging> tinventory900@gmail.com'