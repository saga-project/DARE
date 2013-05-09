from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from invitation.views import request_invite, approve_invite

urlpatterns = patterns('',
    url(r'^complete/$', TemplateView.as_view(template_name='invitation/invitation_complete.html'), name='invitation_complete'),
    url(r'^invited/(?P<invitation_key>\w+)/$', approve_invite, name='invitation_invited'),
    url(r'^request/$', request_invite, name='request_invite')

)
