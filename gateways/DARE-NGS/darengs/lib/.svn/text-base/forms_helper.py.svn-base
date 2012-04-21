# used for the django forms
#from django.db import models
import darengs.lib.forms as forms
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.forms.widgets import RadioSelect,Select
import django.http
from darengs.lib.forms import ModelForm
import os

DARENGS_HOME = os.getcwd()

# go into lib/forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField( widget=forms.PasswordInput, label="Password" )

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


class old_bfastForm(forms.Form):
    description       = forms.CharField()
    #email             = forms.EmailField()
    appname           = forms.CharField(widget=forms.HiddenInput,initial='bfast')

    availgenome_label = 'Choose one of the following genome as a reference geonome'
    availgenome       = [['hg18','Human Genome(hg18)'],['hg18-chromosome21',  \
                        'Human Genome (hg18) chromosome 21'],['BGR1','Microbe BGR1 genome']\
                        ,['new-ref-genome','New Genome from a user'],]
    Reference_GENOME  = forms.ChoiceField( widget=Select(), label = 'Choose Reference Genome' \
                        ,choices=availgenome)
    availdataloc      = [['work','Work'], ['project','Project']]
    Sequence_Location = forms.ChoiceField( widget=Select(), label = \
                        'Choose Short Reads Location', choices=availdataloc)
    machines_label    = 'Resource'
    machines_list     = [['qb','Queen Bee(LONI)'],['ranger','Ranger(XD)'],['kraken','Kraken(XD)'],
                        ['painter','Painter(LONI)'],['fgeuca','FutureGrid(Cloud)'],\
                        ['aws','AWS(Cloud)']]
    machine           = forms.ChoiceField(widget=Select(), label = machines_label, \
                        choices=machines_list)


class bfastForm(forms.Form):

    description       = forms.CharField(initial='put your job description here', \
                        widget=forms.TextInput(attrs={'size':'50'}) )

    appname           = forms.CharField(widget=forms.HiddenInput,initial='chipseq')

    availgenome_label = 'Choose one of the following genome as a reference geonome'
    availgenome       = [['hg19',' Human (hg19)'],
                         ['hg18',' Human (hg18)'],
                         ['mm9','Mouse (mm9)'],
                         ['ws200','C. Elegans (WS200)'],
                         ['bgr1','B. Glumae (BGR1)'],
                         ['yeast','yeast']
                        ]
    Reference_GENOME  = forms.ChoiceField( widget=Select(), label = 'Choose Reference Genome' \
                        ,choices=availgenome, initial = 'hg19')


    mapping_tools = [['BWA','BWA'],['BOWTIE','BOWTIE'],['BFAST','BFAST'],
                     ['Stampy','Stampy'],
                     ['SHRiMP2','SHRiMP2'],['SOAP2','SOAP2'],
                     ['Novoalign','Novoalign'],
                     ['MAQ','MAQ']
                    ]
    mapping           = forms.ChoiceField(widget=Select(), label="Choose Mapping Tool",\
                        choices=mapping_tools, initial =mapping_tools[0][0])

    colorspace     = forms.ChoiceField(widget=Select(), \
                         label = "Color Space",choices=[['false','No'], \
                         ['true','Yes']], initial= 'False' )

    pairedend     = forms.ChoiceField(widget=Select(), \
                         label = "Paired End",choices=[['false','No'], \
                         ['true','Yes']], initial= 'False' )



    chipseq_data = []
    try:
        dirlist = os.listdir(os.path.join( "/home/cctsg/NGSDATA/user_input"))
        for fname in dirlist:
            if not fname.startswith("."):
                chipseq_data.append([fname,fname])
    except:
        chipseq_data.append(["test.fastq","test.fastq"])


    main_input_name = forms.ChoiceField( widget=Select(), label = 'Choose the data for input', \
                        choices=chipseq_data, initial= chipseq_data[0][0])

    chipseq_data.append(["None","None"])

    second_input_name   = forms.ChoiceField( widget=Select(), label = 'Choose the 2nd data for input', \
                        choices=chipseq_data, initial= "None")

    job_size            = forms.ChoiceField(widget=Select(), label="Expected Computation Load",\
                         choices=[["small", "Small (Local)"], ["medium","Medium (Local Cluster)"],["large","Large (HPC Cluster)"] ,["cloud","AWS Cloud"]], \
                         initial= 'small')



class tophatfusionForm(forms.Form):
    description       = forms.CharField()
    #email             = forms.EmailField()
    appname           = forms.CharField(widget=forms.HiddenInput,initial='tophatfusion')

    availgenome_label = 'Choose one of the following genome as a reference geonome'
    availgenome       = [['hg18','Human Genome(hg19)'], ['new-ref-genome','New Genome from a user']]
    Reference_GENOME  = forms.ChoiceField( widget=Select(), label = 'Choose Reference Genome' \
                        ,choices=availgenome)
    availdataloc      = [['cyder','Cyder'], ['work','Work(coming soon)'], \
                        ['project','Project(coming soon)']]
    Sequence_Location = forms.ChoiceField( widget=Select(), label = 'Choose Short Reads Location', \
                        choices=availdataloc)

    machines_label    = 'Resource'
    machines_list     = [['cyder','Cyder'], \
                        ['qb','Queen Bee(coming soon)'],\
                        ['ranger','Ranger(coming soon)'], \
                        ['kraken','Kraken(coming soon)'], \
                        ['painter','Painter(coming soon)'],\
                        ['fgeuca','FutureGrid(Cloud,(coming soon))'],\
                        ['aws','AWS(Cloud,(coming soon))']]
    machine           = forms.ChoiceField(widget=Select(), label=machines_label,\
                        choices=machines_list)


class chipseqForm(forms.Form):

    description       = forms.CharField(initial='put your job description here', \
                        widget=forms.TextInput(attrs={'size':'50'}) )

    appname           = forms.CharField(widget=forms.HiddenInput,initial='chipseq')

    availgenome_label = 'Choose one of the following genome as a reference geonome'
    availgenome       = [['hg19',' Human (hg19)'],
                         ['hg18',' Human (hg18)'],
                         ['mm9','Mouse (mm9)'],
                         ['ws200','C. Elegans (WS200)'],
                         ['bgr1','B. Glumae (BGR1)'],
                         ['yeast','yeast']
                        ]
    Reference_GENOME  = forms.ChoiceField( widget=Select(), label = 'Choose Reference Genome' \
                        ,choices=availgenome, initial = 'hg19')


    mapping_tools = [['BWA','BWA'],['BOWTIE','BOWTIE'],['BFAST','BFAST'],
                     ['Stampy','Stampy'],
                     ['SHRiMP2','SHRiMP2'],['SOAP2','SOAP2'],
                     ['Novoalign','Novoalign'],
                     ['MAQ','MAQ']
                    ]
    mapping           = forms.ChoiceField(widget=Select(), label="Choose Mapping Tool",\
                        choices=mapping_tools, initial =mapping_tools[0][0])

    colorspace     = forms.ChoiceField(widget=Select(), \
                         label = "Color Space",choices=[['false','No'], \
                         ['true','Yes']], initial= 'False' )

    peakcall_tools = [['MACS','MACS'],['Peak Seq','PeakSeq'],]
    peakcall           = forms.ChoiceField(widget=Select(), label="Choose Peak Calling Tool",\
                        choices=peakcall_tools, initial= 'MACS')



    chipseq_data = []
    try:
        dirlist = os.listdir(os.path.join( "/home/cctsg/NGSDATA/user_input"))
        for fname in dirlist:
            if not fname.startswith("."):
                chipseq_data.append([fname,fname])
    except:
        chipseq_data.append(["test.fastq","test.fastq"])

    control_input_name = forms.ChoiceField( widget=Select(), label = 'Choose Control data for input', \
                        choices=chipseq_data, initial= chipseq_data[0][0])


    treat_input_name   = forms.ChoiceField( widget=Select(), label = 'Choose Treat data for input', \
                        choices=chipseq_data, initial= chipseq_data[0][0])

    job_size            = forms.ChoiceField(widget=Select(), label="Expected Computation Load",\
                         choices=[["small", "Small (Local)"], ["medium","Medium (Local Cluster)"],["large","Large (HPC Cluster)"] ,["cloud","AWS Cloud"]], \
                         initial= 'small')










    """
    machines_label    = 'Resource'
    machines_list     = [['cyder','Cyder'], \
                        ['qb','Queen Bee(coming soon)'],\
                        ['ranger','Ranger(coming soon)'], \
                        ['kraken','Kraken(coming soon)'], \
                        ['painter','Painter(coming soon)'],\
                        ['fgeuca','FutureGrid(Cloud,(coming soon))'],\
                        ['aws','AWS(Cloud,(coming soon))']]
    machine           = forms.ChoiceField(widget=Select(), label=machines_label,\
                        choices=machines_list)


    #def __init__(self, *args, **kwargs):
     #   extra = kwargs.pop('extra')
      #  super(chipseqForm, self).__init__(*args, **kwargs)
         #for i, question in enumerate(extra):
          #   self.fields['custom_%s' % i] = forms.CharField(label=question)

#         def extra_answers(self):
 #       for name, value in self.cleaned_data.items():
  #          if name.startswith('custom_'):
   #             yield (self.fields[name].label, value)
    """
