from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#social auth customization
urlpatterns = patterns('main.views',
    url(r'^error/$', 'error', name='error'),
    url(r'^formusername/$', 'formusername', name='formusername'),
    url(r'^formemail/$', 'formemail', name='formemail'),
)
