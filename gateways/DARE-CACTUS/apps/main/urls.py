from django.conf.urls import patterns, url
#social auth customization
urlpatterns = patterns('main.views',
    url(r'^error/$', 'error', name='error'),
    url(r'^check_valid_key/$', 'check_valid_key', name='dare_registration'),
)
