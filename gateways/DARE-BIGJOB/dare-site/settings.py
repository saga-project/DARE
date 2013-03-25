from .default_settings import *
import os

try:
    if os.environ.get('DEVELOPMENT'):
        from env_settings.local.settings import *
    else:
        from env_settings.local.settings import *
except:
    print 