from django import forms
from .models import UserContext, UserResource
import datetime
from django.forms.widgets import Select
from darewap.models import Job, JobInfo, JobDetailedInfo
from .tasks import add_dare_job

import django_tables2 as tables

time_list = [[10, 10]]


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
        job = Job(user=request.user, status="New", title=self.cleaned_data['title'])
        #import pdb;pdb.set_trace()
        job.save()
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
    pass

    def save(self, request):
        pass


class daslkd():
    def __init__(self, user, *args, **kwargs):
        super(ResourceEditConf, self).__init__(*args, **kwargs)
        self.fields['pilot'].queryset = UserResource.objects.filter(user=user)
        self.fields['pilot'].error_messages['required'] = 'Please select a Resource or Create a new resource'

        #self.fields['thornlist'].queryset = Thornfiles.objects.filter(user=user)
        #self.fields['thornlist'].error_messages['required'] = 'Please select a Thornfile or upload Thornfiles in Manage Thorn List'

    def save(self, request):
        job = Job(user=request.user, status="New", name=self.cleaned_data['name'])
        job.save()
        for key, value in self.cleaned_data.items():
                jobinfo = JobInfo(key=key, value=value, job=job)
                jobinfo.save()
        add_dare_job.delay(job)
        return job
