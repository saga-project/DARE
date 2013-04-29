import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dare-site.settings")

import site
site.addsitedir('/opt/dare-virtualenvs/envdarecactus/lib/python2.6/site-packages/easy-install.pth')
site.addsitedir('/opt/dare-virtualenvs/envdarecactus/lib64/python2.6/site-packages/easy-install.pth')
# This application object is used by the development server
# as well as any WSGI server configured to use this file.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
