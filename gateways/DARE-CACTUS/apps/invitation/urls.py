from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from invitation.views import request_invite, approve_invite

urlpatterns = patterns('',
    url(r'^complete/$', direct_to_template, {'template': 'invitation/invitation_complete.html'}, name='invitation_complete'),
    url(r'^invited/(?P<invitation_key>\w+)/$', approve_invite, name='invitation_invited'),
    url(r'^request/$', request_invite, name='request_invite')

)
