# Django settings for ly project.
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

ADMINS = (
    ('thewayiam', 'twly.tw@gmail.com'),
)

SECRET_KEY = 'some_random_secrect'

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#   'django.middleware.security.SecurityMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'ly.urls'

WSGI_APPLICATION = 'ly.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.admin',
    'social.apps.django_app.default',
    'haystack',
    'json_field',
    'legislator',
    'candidates',
    'committees',
    'sittings',
    'vote',
    'bill',
    'search',
    'standpoint',
    'commontag',
    'pagination',
    'rest_framework',
    'debug_toolbar',
)

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'PAGINATE_BY': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                'legislator.context_processor.current_url',
                'legislator.context_processor.district_list',
                'legislator.context_processor.committee_list',
                'legislator.context_processor.distinct_progress_of_bill',
                'legislator.context_processor.party_list',
            ],
        },
    },
]

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

SITE_DOMAIN = 'http://twly.herokuapp.com'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'twly',
    },
}

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
)

LOGIN_URL = '/login/facebook/'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

try:
    from local_settings import *
except ImportError:
    pass
