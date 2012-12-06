from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('darewap.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cactus/', include('cactus.urls')),
    url(r'', include('invitation.urls')),
    url(r'^invite/', include('invitation.urls')),
)
urlpatterns += patterns('',   url(r'', include('social_auth.urls')))
