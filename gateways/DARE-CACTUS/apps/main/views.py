from social_auth.utils import setting
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from social_auth.models import UserSocialAuth
from invitation.models import InvitationKey
is_key_valid = InvitationKey.objects.is_key_valid


user_exists = UserSocialAuth.simple_user_exists

import django
version = django.VERSION


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('socialauth/error.html', {'version': version, 'messages': messages},
                              RequestContext(request))


def check_valid_key(request):
    if not user_exists(username=request.session.get("saved_username")):
        if request.session.get('invitation_key') and is_key_valid(request.session['invitation_key']):
            name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
            backend = dict(request.session)[name]['backend']
            #InvitationKey.get_key(request.session['invitation_key']).mark_used()
            return redirect('socialauth_complete', backend=backend)
        else:
            return render_to_response('invitation/wrong_invitation_key.html', {}, RequestContext(request))
