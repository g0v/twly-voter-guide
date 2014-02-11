"""Local test settings and globals which allows us to run our
test suite locally."""
from .settings import *

########## Just for test only
SECRET_KEY = 'w%3uknhc-5l1nmmh7tp#@29!nthqvc2fb#&!r#x(1(!0ixpwo'
########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = PROJECT_ROOT
TEST_DISCOVER_ROOT = PROJECT_ROOT
TEST_DISCOVER_PATTERN = "*"
