import time
import mimetypes
import sys
import getopt
import django.http
import logging
import commands


import darehthp.model as model
import darehthp.model.meta as meta
import darehthp.lib.forms as forms

from darehthp.lib.forms import ModelForm
from darehthp.lib.base import BaseController, render


from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from darehthp.lib.base import BaseController, render
import darehthp.lib.helpers as h

# used for the django forms
from django.db import models
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings

from webhelpers import paginate

#meta.Session.query(model.Job)


log = logging.getLogger(__name__)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Password" )

class RegisterForm(forms.Form):
    organization = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Your Password" )
    #repassword = forms.CharField( widget=forms.PasswordInput, label="Retype Your Password" )




# used to import the hash library.
try:
    import hashlib
    hash_md5  = hashlib.md5
    hash_sha1 = hashlib.sha1
except:
    import md5
    import sha
    hash_md5 = md5.new
    hash_sha1 = sha.new

#used to encrypt the password and store int he databas#
def hash_password(password, salt):
    m = hashlib.sha256()
    m.update(password)
    m.update(salt)
    return m.hexdigest()

#this method is used to decrypt the password to compare it with encrypted password it. #todo implement it.
def gen_hash_password(password):
    import random
    letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    p = ''
    random.seed()
    for x in range(32):
        p += letters[random.randint(0, len(letters)-1)]
    return hash_password(password, p), p

def authenticate_user(email, password):
    auth_user = meta.Session.query(model.user)
    try:

        a_user = auth_user.filter(model.user.email == str(email)).one()
        print a_user.id
    except:
        print "except"
        return "invalid"

    if (a_user.password != str(password)):
        print "epass"
        return "invalid"

    print "hell2",a_user.id
    return a_user.id

def validate_email(email):
    auth_user = meta.Session.query(model.user)
    try:
        a_user = auth_user.filter(model.user.email == str(email)).one()
    except:
        return 0
    return 1

class UsersController(BaseController):

    # before start using the controller check f the user is logged in and update the user id session variable which is used in the
    #base.mako file to change the display like login, logout etc.,
    def __before__(self, action, **params):
        user = session.get('userid')
        c.display_message =""

        if user:
            request.environ['REMOTE_USER'] = user
            c.userid = user
            print "userid: %s"%user
        else:
            c.userid = "false"
    def __init__(self):
         c.email = ""
         c.login = ""


    def index(self):
        redirect(url('/'))

    def login(self):
        #h.flash('Please login')

        if 'm' in request.params:
           m = request.params['m']
           if (int(m) ==1):
               c.display_message = "Please log in before you submit a job "
           if (int(m) ==2):
               c.display_message = "Please log out before you login "
           if (int(m) ==4):
               c.display_message = "Please log in before you delete a job "

        elif (c.userid != "false"):
             redirect(url('/users/login?m=2'))

        c.form = LoginForm()
        return render('/users/login.mako')

    def register(self):
        if 'm' in request.params:
            m = request.params['m']

            if (int(m) ==3):
                c.display_message = "Please log out before you register "
        elif (c.userid != "false"):
             redirect(url('/users/regitser?m=3'))

        c.form = RegisterForm()
        return render('/users/register.mako')

    def login_validate(self):
        if (c.userid != "false"):
             redirect(url('/users/login?m=2'))
        session['logged_in'] = True
        session.save()

        if request.method == 'POST':
            c.form = LoginForm(request.POST)
            if c.form.is_valid():

                userid = authenticate_user(c.form.cleaned_data['email'], \
                         c.form.cleaned_data['password'])
                print "hellooooo", c.form.cleaned_data['email'], c.form.cleaned_data['password']
                if (userid != "invalid" ):
                    session['userid'] = userid
                    session.save()
                    print session['userid']
                    redirect(url('/'))
                    c.login = "valid"
                else:
                 c.login = "invalid"

            else:
                 c.form = LoginForm(request.POST)

        return render("/users/login.mako")

    def logout(self):
        session.clear()
        session.save()
        redirect(url('/'))

    def register_post(self):
        if (c.userid != "false"):
             redirect(url('/users/register?m=3'))

        if request.method == 'POST':
            c.form = RegisterForm(request.POST)
            if c.form.is_valid():
                newuser= model.user()
                # check to see if email allready exists
                email_users = meta.Session.query(model.user)

                if (validate_email(c.form.cleaned_data['email'])):
                    c.email = "invalid"
                    print "invalid email"
                    return render("/users/register.mako")


                newuser.email = c.form.cleaned_data['email']

                newuser.organization = c.form.cleaned_data['organization']
                newuser.password =      c.form.cleaned_data['password']
                print "c.form.cleaned_data['password']", c.form.cleaned_data['password']
                newuser.salt =  "salt"
                meta.Session.add(newuser)
                meta.Session.commit()

                return render("/users/succ_register.mako")
            else:
                c.form = RegisterForm(request.POST)
        return render("/users/register.mako")
