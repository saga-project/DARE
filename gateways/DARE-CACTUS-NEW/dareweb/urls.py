# Create your views here.
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('dareweb.views',
    url(r'^$', 'view_home', name='site-homepage'),
    (r'^home/$', 'view_home'),
    (r'^about$', 'view_about'),
    (r'^contact/$', 'view_contact'),
    (r'^software$', 'view_software'),
    (r'^resources/$', 'view_resources'),
    (r'^dare-cactus/$', 'view_dare_cactus'),

)
urlpatterns += staticfiles_urlpatterns()
