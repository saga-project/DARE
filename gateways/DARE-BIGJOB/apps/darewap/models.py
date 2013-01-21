from django.db import models
from django.contrib import admin
from django.conf import settings

import datetime
from django.core.files.storage import FileSystemStorage
import random
import string
from picklefield.fields import PickledObjectField


class Job(models.Model):
    user = models.ForeignKey('auth.User', null=True, related_name='user_jobs')
    title = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=30, blank=True)
    cordination_url = models.CharField(max_length=150, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    @property
    def get_status(self):
        pilots = JobInfo.objects.filter(job=self, itype='pilot')
        if len(pilots) > 0:
            if pilots[0].detail.get('status'):
                return pilots[0].detail.get('status')

        return "New"

    @property
    def get_pilots_detail_info(self):
        pilots = JobInfo.objects.filter(job=self, key='pilot')
        all_pilots = []
        for pilot in pilots:
            pilot_info = UserResource.objects.get(id=pilot.user_resource)
            all_pilots.append(pilot_info)

        return all_pilots

    def create_task(self, user_task_id=None):
        if not user_task_id:
            user_task_id = UserTasks.objects.filter(user=self.user)[0].id

        cu_desc = {"ut_id": user_task_id,  "status": "New"}
        new_jobtask = JobInfo()
        new_jobtask.job = self
        new_jobtask.itype = 'task'
        new_jobtask.detail = cu_desc
        new_jobtask.save()
        return new_jobtask

    def save_task(self, job_task_id, ut_id=None, cu_desc={}):
        if ut_id:
            cu_desc["ut_id"] = ut_id

        new_jobtask = JobInfo()
        new_jobtask.job = self
        new_jobtask.itype = 'task'
        new_jobtask.detail.update(cu_desc)
        new_jobtask.save()
        return new_jobtask

    def get_pilot_with_ur(self, ur_id):
        jobinfo = JobInfo.objects.filter(job=self, user_resource=ur_id)
        #print self.id, ur_id, "im in get_pilot", len(jobinfo)
        if len(jobinfo) > 0:
            return jobinfo[0]
        else:
            ur = UserResource.objects.get(id=ur_id)
            pilot_compute_description = {"service_url": getattr(ur, "service_url", "fork://localhost"),
                         "working_directory":  getattr(ur, "working_directory", '/tmp/'),
                         "number_of_processes": getattr(ur, "cores_per_node", 1),
                         "processes_per_node": getattr(ur, "processes_per_node", 1),
                         "ur_id": ur.id}

            return self.save_pilot(pilot_compute_description)

    def save_pilot(self, pilot_desc={}):
        ur_id = pilot_desc.get("ur_id", 0)
        pilot_compute_description = {"service_url": pilot_desc.get("service_url", "fork://localhost"),
                     "number_of_processes": pilot_desc.get("number_of_processes", 1),
                     "working_directory":  pilot_desc.get("working_directory", '/tmp/'),
                     "processes_per_node": pilot_desc.get("processes_per_node", 1),
                     "user_resource_id": ur_id}

        ur = UserResource.objects.get(id=ur_id)
        jobinfo_r = JobInfo.objects.filter(job=self, user_resource=ur_id)
        if len(jobinfo_r) > 0:
            jobinfo = jobinfo_r[0]
        else:
            jobinfo = JobInfo()
            jobinfo.job = self
            jobinfo.itype = 'pilot'
            jobinfo.user_resource = ur

        jobinfo.detail = pilot_compute_description
        jobinfo.save()

        return jobinfo

    def __repr__(self):
        return "%s-%s" % (self.id, self.title)

    def __unicode__(self):
        return "%s-%s" % (self.id, self.title)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        self.status = 'New'
        super(Job, self).save(*args, **kwargs)


class JobInfo(models.Model):
    job = models.ForeignKey('Job', null=True, related_name='job_info')
    description = models.CharField(max_length=200, blank=True)
    itype = models.CharField(max_length=200, blank=True)  # task or pilot
    user_resource = models.ForeignKey('UserResource', null=True, related_name='user resource')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    detail = PickledObjectField(null=True)

    def __repr__(self):
        return "%s-%s-%s" % (self.itype, self.user_resource, self.job)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(JobInfo, self).save(*args, **kwargs)


class JobDetailedInfo(models.Model):
    description = models.CharField(max_length=200, blank=True)
    key = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)
    jobinfo = models.ForeignKey('JobInfo', null=True, related_name='job_detailed_info')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    
    def __repr__(self):
        return self.key

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(JobDetailedInfo, self).save(*args, **kwargs)


fs = FileSystemStorage(location="%s" % settings.DEFAULT_USER_CONTEXT_STORAGE)


def get_path(instance, filename, ptype):
    chars = string.letters + string.digits
    name = string.join(random.sample(chars, 8), '')
    extension = filename.split('.')[-1]
    return '%s/%s/%s.%s' % (ptype, instance.user.id, name, extension)


def get_usercert(instance, filename):
    return get_path(instance, filename, 'usercert')


def get_userproxy(instance, filename):
    return get_path(instance, filename, 'userproxy')


ctx_types = (('SSH', 'SSH'), ('X509', 'X509'), ('EC2', 'EC2'))


class UserContext(models.Model):
    '''  saga.Context() properties'''
    user = models.ForeignKey('auth.User', null=True, related_name='user_context')
    type = models.CharField(max_length=30, choices=ctx_types, default='SSH')
    usercert = models.FileField(upload_to=get_usercert, storage=fs, blank=True, null=True)
    userproxy = models.FileField(upload_to=get_userproxy, storage=fs, blank=True, null=True)
    userid = models.CharField(max_length=30, blank=True)
    userkey = models.CharField(max_length=30, blank=True)
    userpass = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(editable=False, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(UserContext, self).save(*args, **kwargs)


class UserContextAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'userid', 'userkey', 'userpass', 'userproxy', 'usercert')

    def save_model(self, *args, **kwargs):
        return super(UserContextAdmin, self).save_model(*args, **kwargs)

admin.site.register(UserContext, UserContextAdmin)


class UserResource(models.Model):
    user = models.ForeignKey('auth.User', null=True, related_name='user_resource')
    name = models.CharField(max_length=10)
    service_url = models.CharField(max_length=256, blank=True)
    data_service_url = models.CharField(max_length=200,  blank=True)
    working_directory = models.CharField(max_length=30, blank=True)
    allocation = models.CharField(max_length=30, blank=True)
    cores_per_node = models.IntegerField(default=1)
    processes_per_node = models.IntegerField(default=1)
    queue = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(UserResource, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.name:
            return self.name
        return str(self.id)


class UserResourceAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_service_url', 'service_url', 'processes_per_node', 'queue', 'modified')

    def save_model(self, *args, **kwargs):
        return super(UserContextAdmin, self).save_model(*args, **kwargs)

admin.site.register(UserResource, UserResourceAdmin)


spmd_type = (('Single', 'single'), ('MPI', 'mpi'))

ppp = """def tasks(NUMBER_JOBS=1):
    tasks = []
    for i in range(NUMBER_JOBS):
        compute_unit_description = {
        "executable": "/bin/echo",
        "arguments": ["Hello", "$ENV1", "$ENV2"],
        "environment": ['ENV1=env_arg1', 'ENV2=env_arg2'],
        "number_of_processes": 4,
        "spmd_variation": "mpi",
        "output": "stdout.txt",
        "error": "stderr.txt"}
        tasks.append(compute_unit_description)
    return tasks
"""


class UserTasks(models.Model):
    user = models.ForeignKey('auth.User', null=True, related_name='user_tasks')
    name = models.CharField(max_length=30)
    executable = models.CharField(max_length=256, blank=True)
    args = models.CharField(max_length=200, blank=True)
    inputfiles = models.CharField(max_length=30, blank=True)
    outputfiles = models.CharField(max_length=30, blank=True)
    env = models.CharField(max_length=30, blank=True)
    spmd_variation = models.CharField(max_length=30, choices=spmd_type, default='single', blank=True)
    num_of_cores = models.CharField(max_length=30, blank=True)
    num_of_processes = models.CharField(max_length=30, blank=True)
    num_of_tasks = models.CharField(max_length=30, blank=True)
    script = models.TextField(blank=True, default=ppp)

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(UserTasks, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.name:
            return self.name
        return str(self.id)


class UserTasksAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'executable', 'args', 'spmd_variation', 'modified')

    def save_model(self, *args, **kwargs):
        return super(UserTasksAdmin, self).save_model(*args, **kwargs)

admin.site.register(UserTasks, UserTasksAdmin)
