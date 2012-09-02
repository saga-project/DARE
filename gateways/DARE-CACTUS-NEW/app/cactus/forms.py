from django import forms
from django.forms.widgets import Select
from .models import Thornfiles

class ThornfilesForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

machines_list = [['queenbee', 'Queen Bee']]
time_list = [['120', '2 Hours'], \
                    ['300', '5 Hours'],\
                    ['600', '10 Hours'],\
                    ['1440', '1 Day'],\
                    ['2879', '2 Days'],\
                    ]

class CactusJobForm(forms.Form):
    description = forms.CharField(initial='test')
    appname = forms.CharField(widget=forms.HiddenInput, initial='cactus')
    appname = forms.CharField(initial='test')
   # thornlist = forms.ModelField(Thornfiles, label='Select Thorn', required=False)
    corecount = forms.CharField(initial=1, label='Core Count')
    parameterfile = forms.FileField(label='Parmeter File', required=False)
    walltime = forms.ChoiceField(widget=Select(), label='Expected Runtime', choices=time_list, initial='2879')
    machine = forms.ChoiceField(widget=Select(), label='Resource', choices=machines_list)
