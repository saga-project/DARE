from django.http import HttpResponseRedirect
from django.http import Http404


def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and \
       kwargs.get('user') is None:
        return HttpResponseRedirect('/formusername/')


def username(request, *args, **kwargs):
                if kwargs.get('user'):
                        username = kwargs['user'].username
                else:
                        username = request.session.get('saved_username')
                return {'username': username}


def redirect_to_form2(*args, **kwargs):
    if not kwargs['request'].session.get('email_address') and not kwargs.get('user').email:
        return HttpResponseRedirect('/formemail/')


def email(request, *args, **kwargs):
    if kwargs.get('user') and request.session.get('email_address'):
        email = request.session['email_address']
        user = kwargs['user']
        user.email = email
        user.save()


def first_name(request, *args, **kwargs):
    if 'saved_first_name' in request.session:
        user = kwargs['user']
        user.first_name = request.session.get('saved_first_name')
        user.save()
