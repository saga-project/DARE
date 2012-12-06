from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from invitation.views import invite, invited

urlpatterns = patterns('',
    url(r'^invite/complete/$',
                direct_to_template,
                {'template': 'invitation/invitation_complete.html'},
                name='invitation_complete'),
    url(r'^invite/$',
                invite,
                name='invitation_invite'),
    url(r'^invited/(?P<invitation_key>\w+)/$',
                invited,
                name='invitation_invited'),
)
