# used for the django forms
#from django.db import models
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.forms.widgets import RadioSelect,Select
import django.http

from darehthp.lib.forms import ModelForm
import darehthp.lib.forms as forms

import os

DARENGS_HOME = os.getcwd()

# go into lib/forms
class NAMDForm(forms.Form):
    #Mandatory form fields

    description       = forms.CharField()
    #Numofbigjobs      = forms.CharField(max_length=2)


    numresources      = forms.ChoiceField(widget=forms.Select(attrs ={'onchange':'OnChange(this.form.numresources);',}), label ='Number of Resources',choices=[[1,1],[2,2],[3,3]],  initial = '1')

    appname           = forms.CharField(widget=forms.HiddenInput,initial='namd')
    formtype          = forms.CharField(widget=forms.HiddenInput,initial='task')

    machines_list     = [['ranger','Ranger(XD)'],['kraken','Kraken(XD)'],
                        ['fgeuca','FutureGrid(Cloud)'],['qb','Queen Bee(LONI)']]
    
    resource_1_name           = forms.ChoiceField(widget=Select(attrs={'class': 'foo1'}), label ='Resource 1 Name',choices=machines_list)
    
    resource_1_size     = forms.CharField(widget=forms.TextInput(attrs={'class': 'foo1'}),label = "Resource 1 Size (cores)", max_length=4, help_text='A size please')
    namd_jobs_num     = forms.ChoiceField(widget=Select(), label ='Number of NAMD jobs',choices=[[1,1],[2,2],[3,3]])

    namd_conf_file      = forms.FileField(label="NAMD conf File")
    
    numfiles = forms.ChoiceField(widget=forms.Select(attrs ={'onchange':'OnChangef(this.form.numfiles);',}), label ='Number Input NAMD Files',choices=[[0,0],[1,1],[2,2],[3,3],[4,4],[5,5]],  initial = '0')  

    
    def __init__(self, *args, **kwargs):
        
        try:
            
            machines_list     = [['ranger','Ranger(XD)'],['kraken','Kraken(XD)'],
                        ['fgeuca','FutureGrid(Cloud)'],['qb','Queen Bee(LONI)']]    
            keys =[]
            keys.append('description')
            keys.append('numresources')
            keys.append('appname')
            keys.append('formtype')
            
            numresources = kwargs.pop('numresources')
            num_files = kwargs.pop('numfiles')
                       
            super(NAMDForm, self).__init__(*args, **kwargs)
                       
            print int(numresources)
            j = int(numresources)

            for i in range(1, j+1):
                
                self.fields['resource_%s_name'%i] = forms.ChoiceField(widget=Select(), label ='Resource %s Name'%i,choices=machines_list)   
                self.fields['resource_%s_size'%i]  = forms.CharField(label = "Resource %s Size (cores)"%i, max_length=4, help_text='A size please')               
           
                keys.append('resource_%s_name'%i)
                keys.append('resource_%s_size'%i) 

            keys.append('namd_jobs_num')
            keys.append('namd_conf_file') 

            keys.append('numfiles')
            
            j = int(num_files)
            
            if (j !=0):
                for i in range(1, j+1):
                    self.fields['namd_file_%s'%i] = forms.FileField(label="NAMD File %s"%i)                    
                    keys.append('namd_file_%s'%i)

            self.fields.keyOrder = keys
        except:
            super(NAMDForm, self).__init__(*args, **kwargs)

class resource_type_Form(forms.Form):
    inftype            = forms.CharField(widget=forms.HiddenInput,initial= 'resource_type')
    infid              = forms.CharField(widget=forms.HiddenInput,initial='0')
    jobid              = forms.CharField(widget=forms.HiddenInput,initial='0')

    resource_type      = forms.ChoiceField(widget=Select(), \
                         label = "Resource Type",choices=[['ssh','SSH'], ['pbs','PBS Pro'], \
                         ['gram','GRAM']], initial = 'ssh')


class gram_resource_Form(forms.Form):

    #Mandatory form fields

    inftype            = forms.CharField(widget=forms.HiddenInput,initial= 'gram_resource')
    infid              = forms.CharField(widget=forms.HiddenInput,initial='0')
    jobid              = forms.CharField(widget=forms.HiddenInput,initial='0')


    machine            = forms.ChoiceField(widget=Select(), \
                         label = "Resource",\
                         choices=[['qb','QB'], ['eric','Eric']] )
    resource_type      = forms.ChoiceField(widget=Select(), \
                         label = "Resource Type",\
                         choices=[['gram','Globus Gram']] )

    #optional form fields if globus get file field  for proxy
#    globus_proxy       = forms.FileField(initial='/full/path/output/')
    walltime           = forms.CharField(initial='0')
    queue              = forms.CharField(initial='Default')
    allocation         = forms.CharField(initial='Default')
    username           = forms.CharField(initial='')
    add_another        = forms.ChoiceField(widget=Select(), \
                         label = "Add another Resource",choices=[['false','False'], \
                         ['true','True']] )



class ssh_resource_Form(forms.Form):

    #Mandatory form fields

    inftype            = forms.CharField(widget=forms.HiddenInput,initial= 'ssh_resource')
    infid              = forms.CharField(widget=forms.HiddenInput,initial='0')
    jobid              = forms.CharField(widget=forms.HiddenInput,initial='0')

    machine            = forms.CharField(initial='Hostname')

    sshpubkey           = forms.CharField(label = "SSH pub key", widget=forms.Textarea, initial='paste your id_rsa.key')
    username           = forms.CharField(initial='')

    #optional form fields if globus get file field  for proxy
    add_another        = forms.ChoiceField(widget=Select(), \
                         label = "Add another Resource",choices=[['false','False'], \
                         ['true','True']] )

class pbs_resource_Form(forms.Form):

    #Mandatory form fields

    inftype            = forms.CharField(widget=forms.HiddenInput,initial= 'pbs_resource')
    infid              = forms.CharField(widget=forms.HiddenInput,initial='0')
    jobid              = forms.CharField(widget=forms.HiddenInput,initial='0')

    sshpubkey          = forms.CharField(label = "SSH pub key", widget=forms.Textarea, initial='paste your id_rsa.key')
    machine            = forms.CharField(initial='Hostname')

    walltime           = forms.CharField(initial='0')
    queue              = forms.CharField(initial='Default')
    allocation         = forms.CharField(initial='Default')


    username           = forms.CharField(initial='')
    add_another        = forms.ChoiceField(widget=Select(), \
                         label = "Add another Resource",choices=[['false','False'], \
                         ['true','True']] )


class wu_Form(forms.Form):

    #Mandatory form fields

    inftype            = forms.CharField(widget=forms.HiddenInput,initial= 'wu')
    infid              = forms.CharField(widget=forms.HiddenInput,initial='0')
    jobid              = forms.CharField(widget=forms.HiddenInput,initial='0')


    ##doc: give full path to executable if possible or provide it env\
    resource_wu        = forms.ChoiceField(widget=Select(), \
                         label = "Preffered Resource",choices=[['any','Any'], ['QB','QB'], \
                         ['ERIC','ERIC']] )
    executable         = forms.CharField(initial='/full/path/executable')
    arguments         = forms.CharField(initial='NULL')
    environment        = forms.CharField(initial='NULL')

    working_directory  = forms.CharField(initial='$HOME/')
    num_cores          = forms.CharField(initial='1')

    spmd_variation      = forms.ChoiceField(widget=Select(), \
                         label = "Type",choices=[['single','Single'], \
                         ['mpi','MPI']] )
    output_dir          = forms.CharField(initial='$HOME')

    #optional fields
    description        = forms.CharField(initial='Hello World', required=False)
    ##doc: input files will be placed in the working directory
#    input_file         = forms.FileField(required=False)
    appname            = forms.CharField(widget=forms.HiddenInput,initial='generic')
    add_another        = forms.ChoiceField(widget=Select(), \
                         label = "Add another Work Unit",choices=[['false','False'], \
                         ['true','True']] )
