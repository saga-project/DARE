from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('darewap.views',
    url(r'^$', 'view_home', name='site-homepage'),
    (r'^view-job-list/$', 'view_job_list'),
    (r'^logout/$', 'view_logout'),
    (r'^login/$', 'view_login_all'),
    (r'^static/(?P<page_type>[-\w]+)/$', 'view_static'),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',   url(r'', include('social_auth.urls')))
