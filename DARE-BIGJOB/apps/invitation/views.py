from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from invitation.models import InvitationKey
from invitation.forms import RequestInvitationKeyForm

is_key_valid = InvitationKey.objects.is_key_valid
remaining_invitations_for_user = InvitationKey.objects.remaining_invitations_for_user


def approve_invite(request, invitation_key=None, extra_context=None):
    if getattr(settings, 'INVITE_MODE', False):
        if invitation_key and is_key_valid(invitation_key):
            template_name = 'invitation/invited.html'
        else:
            template_name = 'invitation/wrong_invitation_key.html'
            return render_to_response(template_name, RequestContext(request, extra_context))

        extra_context = extra_context is not None and extra_context.copy() or {}
        extra_context.update({'invitation_key': invitation_key})
        request.session['invitation_key'] = invitation_key

        return HttpResponseRedirect(reverse('dare_login'))
    else:
        return HttpResponseRedirect(reverse('dare_login'))


def request_invite(request, form_class=RequestInvitationKeyForm, extra_context={}):

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('invitation_complete'))
    else:
        form = form_class()
        extra_context.update({'form': form})

    template_name = 'invitation/invitation_form.html'
    return render_to_response(template_name, RequestContext(request, extra_context))
