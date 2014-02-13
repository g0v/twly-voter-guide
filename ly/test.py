"""Local test settings and globals which allows us to run our
test suite locally."""
from os.path import join, abspath, dirname


here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")

########## Just for test only
SECRET_KEY = 'w%3uknhc-5l1nmmh7tp#@29!nthqvc2fb#&!r#x(1(!0ixpwo'
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'ly', # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '', # Set to empty string for default.
            'TEST_CHARSET':'UTF8'
            }
        }
########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT
TEST_DISCOVER_ROOT = PROJECT_ROOT
TEST_DISCOVER_PATTERN = "*"


from .settings import *
