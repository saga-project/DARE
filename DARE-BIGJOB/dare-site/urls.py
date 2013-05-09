from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('darewap.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('invitation.urls')),
    url(r'^invite/', include('invitation.urls')),
)
urlpatterns += patterns('',   url(r'', include('social_auth.urls')))

if settings.DEBUG == False:
    urlpatterns += patterns('',
                url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': False})
        )
