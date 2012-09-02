from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('darewap.views',
    url(r'^$', 'view_home', name='site-homepage'),
    (r'^home/$', 'view_home'),
    (r'^about$', 'view_about'),
    (r'^contact/$', 'view_contact'),
    (r'^software$', 'view_software'),
    (r'^resources/$', 'view_resources'),
    (r'^dare-cactus/$', 'view_dare_cactus'),
    (r'^login/$', 'view_login'),
    (r'^logout/$', 'view_logout'),
    (r'^view_job_list/$', 'view_job_list'), 
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',   url(r'', include('social_auth.urls')))
