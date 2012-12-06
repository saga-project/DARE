from django.shortcuts import render_to_response
from django.template import RequestContext
from social_auth.models import UserSocialAuth
from invitation.models import InvitationKey
is_key_valid = InvitationKey.objects.is_key_valid
user_exists = UserSocialAuth.simple_user_exists


#def check_valid_key(request, *args, **kwargs):
#    request.session["saved_username"] = kwargs.get('username')
#    return HttpResponseRedirect('/check_valid_key/')


def check_valid_key(request, *args, **kwargs):
    print kwargs.get('username')
    if not user_exists(username=kwargs.get('username')):
        if request.session.get('invitation_key') and is_key_valid(request.session['invitation_key']):
            pass
            #InvitationKey.get_key(request.session['invitation_key']).mark_used()
        else:
            return render_to_response('invitation/wrong_invitation_key.html', {}, RequestContext(request))
