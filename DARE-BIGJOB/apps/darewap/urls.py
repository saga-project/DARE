from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = patterns('darewap.views',
    url(r'^$', RedirectView.as_view(url='/runs/')),

    url(r'^home/$', 'view_home', name='site-homepage'),
    url(r'^view-job-list/$', 'view_job_list'),
    url(r'^logout/$', 'view_logout'),
    url(r'^login/$', 'view_login_all', name='dare_login'),
    url(r'^log-in/$', 'view_login', name='dare_login_in'),
    url(r'^stat/(?P<page_type>[-\w]+)/$', 'view_static'),
    url(r'^login/$', 'view_login_all', name='request_invite'),
    url(r'^accounts/contexts/$', 'view_manage_contexts', name='manage_contexts'),
    url(r'^accounts/resources/$', 'view_manage_resources', name='manage_rsources'),
)


urlpatterns += patterns('darewap.views',
    url(r'^my-tasks/$', 'view_manage_tasks', name='managetasks'),
    url(r'^my-pilots/$', 'view_manage_pilots', name='managepilots'),

    url(r'^job/bigjob/$', 'view_bigjob', name='bigjob'),
    url(r'^job/celery_tasks/$', 'view_celery_tasks', name='celery_tasks'),
    url(r'^job/create/$', 'view_create_job_bigjob', name='createbigjob'),
    url(r'^job/pilot_popup/(?P<job_id>[-\w]+)/(?P<ur_id>[-\w]+)/$', 'view_pilot_popup', name='pilot_popup'),
    url(r'^job/task_popup/(?P<job_id>[-\w]+)/(?P<job_task_id>[-\w]+)/$', 'view_pilot_popup', name='task_popup'),

    url(r'^job/tasks/$', 'view_job_tasks', name='createtasks'),
    url(r'^job-actions/$', 'view_job_actions', name='jobactions'),

    #new urls
    url(r'^runs/$', 'view_all_dare_runs', name='dare_runs'),
    url(r'^runs/new/$', 'view_create_run', name='create_dare_run'),
    url(r'^runs/(?P<id>\d+)/$', 'view_dare_run', name='dare_run'),

    )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
