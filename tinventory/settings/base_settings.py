import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    
    # Built-in / Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Repository Apps
    'transformations',
    'resources',
    'topics',
    'people',
    'sitepages',
    
    # 3rd Party Packages
    'widget_tweaks',
    'autoslug',
    'stronghold',
    'mptt',
    'django_mptt_admin',
    'termsandconditions',
    #'applicationinsights',
    #'storages',
    
    # Wagtail Packages
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',
    'modelcluster',
    'taggit',

]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
    'people.middleware.SetLastVisitMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    #'termsandconditions.middleware.TermsAndConditionsRedirectMiddleware',
    #'applicationinsights.django.ApplicationInsightsMiddleware',
]

ROOT_URLCONF = 'tinventory.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'topics.context_processors.add_topics',
            ],
        },
    },
]

WSGI_APPLICATION = 'tinventory.wsgi.application'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

#NB: Had to run "pip install mysqlclient"


# Authorization

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'tinventory.core.authentication.EmailAuthBackend',
    )

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Canada/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static') 
# To run collectstatic, comment out line 2 and uncomment line 3 above.

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = '/login/'

AUTH_USER_MODEL = 'auth.User'
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/users/%s/" % u.username,
}

# EMAIL

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "tinventory900@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#WAGTAIL
WAGTAIL_SITE_NAME = 'Transformation Repository'

#STRONGHOLD
STRONGHOLD_DEFAULTS = True
STRONGHOLD_PUBLIC_NAMED_URLS = ('login', 'password_reset', 'password_reset_done', 'password_reset_confirm', 'password_reset_complete')
STRONGHOLD_PUBLIC_URLS = (r'^/__debug__/.+$',)

# TERMS AND CONDITIONS
TERMS_BASE_TEMPLATE = 'core/base_card.html'
ACCEPT_TERMS_PATH = '/terms/accept/'
TERMS_CACHE_SECONDS = 30