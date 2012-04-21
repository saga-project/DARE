# used for the django forms
#from django.db import models
import darecactus.lib.forms as forms
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.forms.widgets import RadioSelect,Select
import django.http
from darecactus.lib.forms import ModelForm
import os

DARENGS_HOME = os.getcwd()

# go into lib/forms



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Password" )
    redirect = forms.CharField(widget=forms.HiddenInput,initial='null', required = False)
    def __init__(self, *args, **kwargs):
        try:
            redirect = kwargs.pop('redirect')
            super(LoginForm, self).__init__(*args, **kwargs)

            self.fields['redirect'] = forms.CharField(widget=forms.HiddenInput,initial=redirect, required = False)

        except:
            super(LoginForm, self).__init__(*args, **kwargs)
        
class RegisterForm(forms.Form):
    organization = forms.CharField()
    email = forms.EmailField()
    #password = forms.CharField( widget=forms.PasswordInput, label="Your Password" )
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,label="Retype Password")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
