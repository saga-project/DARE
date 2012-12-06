from social_auth.utils import setting
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


import django
version = django.VERSION


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('socialauth/error.html', {'version': version, 'messages': messages},
                              RequestContext(request))

from invitation.models import InvitationKey
is_key_valid = InvitationKey.objects.is_key_valid


def formusername(request):
        if request.method == 'POST' and request.POST.get('username') and request.session.get('invitation_key'):
                if is_key_valid(request.session['invitation_key']):
                        if (not User.objects.filter(username=request.POST['username']).exists()):
                                name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
                                request.session['saved_username'] = request.POST['username']
                                backend = request.session[name]['backend']
                                return redirect('socialauth_complete', backend=backend)
                        else:
                                return render_to_response('socialauth/form.html', {'error': ('Username already exists!')}, RequestContext(request))
                else:
                        render_to_response('socialauth/form.html', {'error': ('Invalid Invitation Key')}, RequestContext(request))
        return render_to_response('socialauth/form.html', {}, RequestContext(request))


def formemail(request):
    if request.method == 'POST' and request.POST.get('email_address'):
        request.session['email_address'] = request.POST['email_address']
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('socialauth/form2.html', {}, RequestContext(request))
