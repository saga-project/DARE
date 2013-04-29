from django import forms
from .models import UserContext, UserResource
import datetime

import django_tables2 as tables


class UserContextForm(forms.ModelForm):
    class Meta:
        model = UserContext
        exclude = ('user')

    def save(self, commit=True, *args, **kwargs):
        request = kwargs.pop('request')
        self.instance.user = request.user
        self.instance.created = datetime.datetime.now()
        self.instance.modified = datetime.datetime.now()

        super(UserContextForm, self).save(commit=commit, *args, **kwargs)


class UserContextTable(tables.Table):
    class Meta:
        model = UserContext
        exclude = ('user', 'created')


class UserResourceForm(forms.ModelForm):
    class Meta:
        model = UserResource
        exclude = ('user', 'modified')

    def save(self, commit=True, *args, **kwargs):
        request = kwargs.pop('request')
        self.instance.user = request.user
        self.instance.created = datetime.datetime.now()
        self.instance.modified = datetime.datetime.now()

        super(UserResourceForm, self).save(commit=commit, *args, **kwargs)


class UserResourceTable(tables.Table):
    class Meta:
        model = UserResource
        exclude = ('user', 'created')
