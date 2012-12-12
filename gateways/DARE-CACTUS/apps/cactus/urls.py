from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('cactus.views',
    url(r'^thornfileslist/$', 'view_thornfileslist', name='thornfileslist'),
    url(r'^create-job/$', 'view_create_job_cactus', name='createjobcactus'),
    url(r'^job-actions/$', 'view_job_actions', name='jobactions'),)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
