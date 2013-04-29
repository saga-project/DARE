from django.shortcuts import render_to_response
from django.template import RequestContext
from social_auth.models import UserSocialAuth
from invitation.models import InvitationKey
from django.contrib.auth.models import User

is_key_valid = InvitationKey.objects.is_key_valid
user_exists = UserSocialAuth.simple_user_exists
get_key = InvitationKey.objects.get_key


def check_valid_key(request, *args, **kwargs):
    print kwargs.get('username')
    if not user_exists(username=kwargs.get('username')):
        if request.session.get('invitation_key') and is_key_valid(request.session['invitation_key']):
            return {}
        else:
            return render_to_response('invitation/wrong_invitation_key.html', {}, RequestContext(request))


def mark_used_key(request, *args, **kwargs):
    if kwargs.get('is_new'):
        inv_key = get_key(request.session.get('invitation_key'))
        user = User.objects.get(username=kwargs.get('username'))
        inv_key.mark_used(user)
