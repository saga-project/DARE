from django import forms
from .models import DareBigJobTask
import datetime
time_list = [[10, 10]]


class UserTasksForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
     #   initial = kwargs.get('initial', {})
     #   initial['script'] = ppp
     #   kwargs['initial'] = initial
     #   super(UserTasksForm, self).__init__(*args, **kwargs)
     #   #self.fields['spmd_variation'] = forms.ChoiceField(widget=Select(), choices=spmd_type, initial='10')

    class Meta:
        model = DareBigJobTask
        exclude = ('user')

    def save(self, commit=True, *args, **kwargs):
        request = kwargs.pop('request')
        self.instance.user = request.user
        self.instance.created = datetime.datetime.now()
        self.instance.modified = datetime.datetime.now()
        return super(UserTasksForm, self).save(commit=commit, *args, **kwargs)
