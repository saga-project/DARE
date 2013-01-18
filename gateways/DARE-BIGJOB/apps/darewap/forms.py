from django import forms
from .models import UserContext, UserResource, UserTasks, spmd_type
import datetime
from django.forms.widgets import Select
from darewap.models import Job, JobInfo, JobDetailedInfo
from .tasks import add_dare_job

import django_tables2 as tables

time_list = [[10, 10]]


class UserTasksForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
     #   initial = kwargs.get('initial', {})
     #   initial['script'] = ppp
     #   kwargs['initial'] = initial
     #   super(UserTasksForm, self).__init__(*args, **kwargs)
     #   #self.fields['spmd_variation'] = forms.ChoiceField(widget=Select(), choices=spmd_type, initial='10')

    class Meta:
        model = UserTasks
        exclude = ('user')

    def save(self, commit=True, *args, **kwargs):
        request = kwargs.pop('request')
        self.instance.user = request.user
        self.instance.created = datetime.datetime.now()
        self.instance.modified = datetime.datetime.now()
        #import pdb;pdb.set_trace()
        return super(UserTasksForm, self).save(commit=commit, *args, **kwargs)


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


class PilotForm(forms.Form):
    title = forms.CharField(initial='test')
    jobid = forms.CharField(initial='0')
    #thornlist = forms.ModelChoiceField(Thornfiles, label='Select Thorn')
    #corecount = forms.CharField(initial=1, label='Core Count')
    #walltime = forms.ChoiceField(widget=Select(), label='Expected Runtime', choices=time_list, initial='2879')
    pilots = forms.ModelMultipleChoiceField(UserResource.objects, label='Select Resource')

    def __init__(self, user, *args, **kwargs):
        super(PilotForm, self).__init__(*args, **kwargs)
        self.fields['pilots'].queryset = UserResource.objects.filter(user__isnull=True) | UserResource.objects.filter(user=user)
        self.fields['pilots'].error_messages['required'] = 'Please select atleast one Resource'
        self.fields['title'].widget.attrs['class'] = 'input-medium'

    def save(self, request):
        job = Job.objects.get(id=self.cleaned_data.get('jobid'))
        job.title = self.cleaned_data.get('title')
        for pilot in self.cleaned_data.get('pilots'):
            jobinfo = JobInfo(itype='pilot', job=job)
            jobinfo.user_resource = pilot
            jobinfo.save()

        for jobinfo in JobInfo.objects.filter(itype='pilot', job=job):
            pilot_params = {"walltime": 10, "num_of_cores": pilot.cores_per_node}
            for pilot_param, value in pilot_params.items():
                if not JobDetailedInfo.objects.filter(jobinfo=jobinfo, key=pilot_param):
                    jdi = JobDetailedInfo(key=pilot_param, value=value)
                    jdi.save()

        #add_dare_job.delay(job)
        return job


class ResourceEditConf(forms.Form):
    num_of_cores = forms.CharField(label='Num of Cores', required=False)
    walltime = forms.CharField(initial=100, label='Walltime', required=False)
    #username = forms.CharField(initial=1, label='username', required=False)
    working_directory = forms.CharField(initial=1, label='Working Directory', required=False)
    context = forms.ModelChoiceField(UserContext, label='Select Thorn', required=False)

    def __init__(self, user, *args, **kwargs):
        pilot = kwargs.pop('pilot')
        self.pilot = UserResource.objects.get(id=pilot)
        job_id = kwargs.pop('job_id')
        self.job = Job.objects.get(id=job_id)

        super(ResourceEditConf, self).__init__(*args, **kwargs)
        self.fields['walltime'].widget.attrs['class'] = 'input-medium'
        self.fields['num_of_cores'].widget.attrs['class'] = 'input-medium'
        self.fields['num_of_cores'].initial = self.pilot.cores_per_node
        self.fields['working_directory'].widget.attrs['class'] = 'input-large'
        self.fields['working_directory'].initial = self.pilot.working_directory

    def save(self, request):
        #pilot_params = ["walltime", "num_of_cores"]

        jobinfo, _ = JobInfo.objects.get_or_create(itype='pilot', user_resource=self.pilot, job=self.job)

        for pilot_param, value in self.cleaned_data.items():
            if value is not None:
                jdi, _ = JobDetailedInfo.objects.get_or_create(jobinfo=jobinfo, key=pilot_param)
                jdi.value = value
                jdi.save()
