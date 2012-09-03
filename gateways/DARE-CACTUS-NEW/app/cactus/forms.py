from django import forms
from django.forms.widgets import Select
from .models import Thornfiles, Paramfiles
from darewap.models import Job, JobQueue, JobInfo

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
    description = forms.CharField(initial='Test')
    appname = forms.CharField(initial='test')
    thornlist = forms.ModelChoiceField(Thornfiles, label='Select Thorn')
    corecount = forms.CharField(initial=1, label='Core Count')
    parameterfile = forms.FileField(label='Parmeter File')
    walltime = forms.ChoiceField(widget=Select(), label='Expected Runtime', \
                                choices=time_list, initial='2879')
    machine = forms.ChoiceField(widget=Select(), label='Resource', \
                                choices=machines_list)

    def __init__(self, user, *args, **kwargs):
        super(CactusJobForm, self).__init__(*args, **kwargs)
        self.fields['thornlist'].queryset = Thornfiles.objects.filter(user=user)

    def save(self, request):
        job = Job(user=request.user)
        job.save()
        for key, value in self.fields.items():
            print key, value
            if key == 'parameterfile':
                newdoc = Paramfiles(paramfile=request.FILES['parameterfile'], job=job)
                newdoc.save()
                jobinfo = JobInfo(key=key, value=newdoc.id, job=job)
            else:
                jobinfo = JobInfo(key=key, value=value, job=job)
                jobinfo.save()

        jobq = JobQueue(job=job)
        jobq.save()
        return job

