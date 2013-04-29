from django import forms
from django.forms.widgets import Select
from .models import Thornfiles, Paramfiles
from darewap.models import Job, JobQueue, JobInfo
from .tasks import add_dare_job
from darewap.models import UserResource


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
    name = forms.CharField(initial='test')
    #thornlist = forms.ModelChoiceField(Thornfiles, label='Select Thorn')
    corecount = forms.CharField(initial=1, label='Core Count')
    parameterfile = forms.FileField(label='Parmeter File')
    walltime = forms.ChoiceField(widget=Select(), label='Expected Runtime', \
                                choices=time_list, initial='2879')
    pilot = forms.ModelChoiceField(UserResource.objects, label='Select Resource')

    def __init__(self, user, *args, **kwargs):
        super(CactusJobForm, self).__init__(*args, **kwargs)
        self.fields['pilot'].queryset = UserResource.objects.filter(user=user)
        self.fields['pilot'].error_messages['required'] = 'Please select a Resource or Create a new resource'

        #self.fields['thornlist'].queryset = Thornfiles.objects.filter(user=user)
        #self.fields['thornlist'].error_messages['required'] = 'Please select a Thornfile or upload Thornfiles in Manage Thorn List'

    def save(self, request):
        job = Job(user=request.user, status="New", name=self.cleaned_data['name'])
        job.save()
        for key, value in self.cleaned_data.items():
            if key in ['name']:
                continue
            if key.lower() == 'parameterfile':
                newdoc = Paramfiles(paramfile=request.FILES['parameterfile'], job=job)
                newdoc.save()
                jobinfo = JobInfo(key=key, value=newdoc.id, job=job)
                jobinfo.save()
            else:
                if hasattr(value, 'id'):
                    jobinfo = JobInfo(key=key, value=value.id, job=job)
                else:
                    jobinfo = JobInfo(key=key, value=value, job=job)
                jobinfo.save()

        add_dare_job.delay(job)
        return job
