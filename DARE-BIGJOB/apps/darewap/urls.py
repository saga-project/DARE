from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = patterns('darewap.views',
    url(r'^$', RedirectView.as_view(url='/runs/')),

    url(r'^home/$', 'view_home', name='site-homepage'),
    url(r'^logout/$', 'view_logout'),
    url(r'^login/$', 'view_login_all', name='dare_login'),
    url(r'^log-in/$', 'view_login', name='dare_login_in'),
    url(r'^stat/(?P<page_type>[-\w]+)/$', 'view_static'),
    url(r'^login/$', 'view_login_all', name='request_invite'),
)


urlpatterns += patterns('darewap.views',
    #new urls
    url(r'^runs/$', 'view_all_dare_runs', name='dare_runs'),
    url(r'^runs/new/$', 'view_create_run', name='create_dare_run'),
    url(r'^runs/(?P<id>\d+)/$', 'view_dare_run', name='dare_run'),
    url(r'^runs/(?P<id>\d+)/add-pilot/$', 'view_run_add_pilot', name='dare_run_pilot'),
    url(r'^runs/(?P<id>\d+)/add-task/$', 'view_run_add_task', name='dare_run_task'),
    url(r'^runs/(?P<id>\d+)/action-pilot/$', 'view_run_pilot_celery_action', name='dare_run_pilot'),
    url(r'^runs/(?P<id>\d+)/action-task/$', 'view_run_task_celery_action', name='dare_run_pilot'),
    )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
