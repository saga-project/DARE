from .default_settings import *
import os

try:
    if os.environ.get('APPENV') == 'Development':
        from env_settings.development.settings import *
    else:
        from env_settings.local.settings import *
except:
    print 'error'
