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

from darecactus.lib.cactusormhelper import *

DARENGS_HOME = os.getcwd()

# go into lib/forms
machines_list   =  [\
		#['cyder','Cyder'], \
                    ['queenbee','Queen Bee'],\
                    #['lonestar','Lonestar'],\
                    #['ranger','Ranger'],\
                    #['osg', 'OSG glidein-WMS Pool'],\
                    ]
time_list       = [\
		['120','2 Hours'], \
                    ['300','5 Hours'],\
                    ['600','10 Hours'],\
                    ['1440','1 Day'],\
                    ['2879','2 Days'],\
                    ]

                 
class CactusForm(forms.Form): 
                 
    description     = forms.CharField(initial='test')
    appname         = forms.CharField(widget=forms.HiddenInput,initial='cactus')
    appname         = forms.CharField(initial='test')
    thornlist       = forms.ChoiceField(widget=Select(), label='Select Thorn', required = False)  
    corecount       = forms.CharField(initial=1, label='Core Count')
    parameterfile   = forms.FileField(label='Parmeter File',required = False)              
    walltime        = forms.ChoiceField(widget=Select(), label='Expected Runtime', choices=time_list, initial='2879')   
    machine         = forms.ChoiceField(widget=Select(), label='Resource', choices=machines_list)                        
    
    def __init__(self, *args, **kwargs):
        try:
            thorns = kwargs.pop('thorns')
            super(CactusForm, self).__init__(*args, **kwargs)
            self.fields['thornlist']    = forms.ChoiceField(widget=Select(), label='Select Thorn',\
                        choices=thorns,required = False)  
    
        except:
            super(CactusForm, self).__init__(*args, **kwargs)  
     
          
                        
class ThornForm(forms.Form):
    
    description     = forms.CharField(initial='test')    
    thornfile       = forms.FileField(label='Upload Thorn File', required = False)    
    machines_list   =  [['cyder','Cyder'], \
                        ['qb','Queen Bee'],\
                        ['painter','Painter'],\
                        ['ranger','Ranger'], \
                        ['kraken','Kraken(coming soon)'], \
                        ['fgeuca','FutureGrid(Cloud,(coming soon))'],\
                        ['aws','AWS(Cloud,(coming soon))']] 
    
    #avail_machines  = forms.ChoiceField(widget=RadioSelect(), label='Resource',\
     #                   choices=machines_list)                          
