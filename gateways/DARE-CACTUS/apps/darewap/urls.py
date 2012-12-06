from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('darewap.views',
    url(r'^$', 'view_home', name='site-homepage'),
    url(r'^view-job-list/$', 'view_job_list'),
    url(r'^logout/$', 'view_logout'),
    url(r'^login/$', 'view_login_all', name='dare_login'),
    url(r'^static/(?P<page_type>[-\w]+)/$', 'view_static'),
    url(r'^login/$', 'view_login_all', name='request_invite'),
)
urlpatterns += staticfiles_urlpatterns()
