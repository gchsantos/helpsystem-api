import os

from helpsystem_api.settings.base import *

# Initialise environment variables
DEBUG = False
ALLOWED_HOSTS = ["localhost"]
BASE_DIR = os.path.dirname(os.path.realpath(os.path.dirname(__file__) + "/.."))
