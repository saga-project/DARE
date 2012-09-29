from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('darewap.views',
    (r'^?P<page_type>[^/]+)/$', 'view_static'),
    (r'^view_job_list/$', 'view_job_list'),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',   url(r'', include('social_auth.urls')))
