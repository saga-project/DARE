import time
import mimetypes
import sys
import getopt
import django.http
import logging
import commands


import darecactus.model as model
import darecactus.model.meta as meta
import darecactus.lib.forms as forms

from darecactus.lib.forms import ModelForm
from darecactus.lib.base import BaseController, render


from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from darecactus.lib.base import BaseController, render
import darecactus.lib.helpers as h

from webhelpers import paginate
from darecactus.lib.userformshelper import *
from darecactus.lib.userormhelper import *

#meta.Session.query(model.Job)

log = logging.getLogger(__name__)



class UsersController(BaseController):

    # before start using the controller check if the user is logged in and update the user id session variable which is used in the 
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
        try:
            action = request.params['action']
            controller = request.params['cont']
            redirect_url ='/%s/%s'%(controller, action)
        except:
            redirect_url = 'null'
        print   redirect_url    
        c.form = LoginForm(redirect=redirect_url)
         
        return render('/users/login.mako')

    def register(self):
         
        if (c.userid != "false"):
             redirect(url('/users/regitser'))
        
        c.form = RegisterForm()
        return render('/users/register.mako')

    def login_validate(self):
    
        if (c.userid != "false"):
             redirect(url('/users/login?m=2'))
        session['logged_in'] = True
        session.save()    
            
        if request.method == 'POST':
            loginform = LoginForm(request.POST)
            if   loginform.is_valid():

                userid = authenticate_user(loginform.cleaned_data['email'], \
                         loginform.cleaned_data['password'])

                if (userid != "invalid" ):
                    session['userid'] = userid
                    session.save()
                    print session['userid']
                    c.login = "valid"
                    print loginform.cleaned_data['redirect']
                    if request.POST['redirect']=='null':                  
                        redirect(url('/'))
                    else:
                        redirect(url(str(loginform.cleaned_data['redirect'])))
                else:
                    c.login = "invalid"
                    c.form = LoginForm(request.POST)
                    return render("/users/login.mako")
            else:
                 c.form = LoginForm(request.POST)
                 return render("/users/login.mako")
        redirect(url('/'))
          
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
                   
                registration = add_user(c.form.cleaned_data)   
                # check to see if email allready exists
                
                if (registration == "emailexists"):
                    c.email = "invalid"
                    mess =  "email already exists"
                    return render("/users/register.mako")


                return render("/users/succ_register.mako")
            
            else:
                c.form = RegisterForm(request.POST)
        return render("/users/register.mako")