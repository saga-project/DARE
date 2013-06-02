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

    def get_or_create_jobinfo_for_pilot(self, pilot_id):
        jobinfo = JobInfo.objects.filter(job=self, user_pilot=pilot_id)
        if len(jobinfo) > 0:
            return jobinfo[0]
        else:
            pilot = UserPilots.objects.get(id=pilot_id)
            jobinfo = JobInfo()
            jobinfo.job = self
            jobinfo.itype = 'pilot'
            jobinfo.user_pilot = pilot
            jobinfo.detail = {'status': 'New'}
            jobinfo.save()

        return jobinfo

    def create_jobinfo_for_task(self, task_id):
        task = UserTasks.objects.get(id=task_id)
        jobinfo = JobInfo()
        jobinfo.job = self
        jobinfo.itype = 'task'
        jobinfo.user_task = task
        jobinfo.detail = {'status': 'New'}
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
    #user_resource = models.ForeignKey('UserResource', null=True, related_name='user resource')
    user_pilot = models.ForeignKey('UserPilots', null=True, related_name='jobuserpilots')
    user_task = models.ForeignKey('UserTasks', null=True, related_name='jobusertasks')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
    detail = PickledObjectField(null=True)

    def __repr__(self):
        return "%s-%s" % (self.itype, self.job)

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
    name = models.CharField(max_length=30)
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
        return super(UserResourceAdmin, self).save_model(*args, **kwargs)

admin.site.register(UserResource, UserResourceAdmin)


spmd_type = (('Single', 'single'), ('MPI', 'mpi'))

simple_task_script = """def tasks(NUMBER_JOBS=1):
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
    return tasks"""


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
    script = models.TextField(blank=True, default=simple_task_script)

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


class UserPilots(models.Model):
    user = models.ForeignKey('auth.User', null=True, related_name='user_pilots')
    name = models.CharField(max_length=30)
    detail = PickledObjectField(null=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(UserPilots, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.name:
            return self.name
        return str(self.id)


class UserPilotsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'detail')

    def save_model(self, *args, **kwargs):
        return super(UserPilotsAdmin, self).save_model(*args, **kwargs)

admin.site.register(UserPilots, UserPilotsAdmin)


class BaseDareModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30, null=False, blank=False, default='name')
    status = models.CharField(max_length=30, null=False, blank=False, default='New')
    user = models.ForeignKey('auth.User')

    class Meta:
        abstract = True

    def __unicode__(self):
        if self.name:
            return self.name
        return str(self.id)


class BaseDareBigJobPilot(BaseDareModel):
    pilot_type = models.CharField(max_length=10)
    service_url = models.CharField(max_length=256)
    data_service_url = models.CharField(max_length=256,  blank=True)
    working_directory = models.CharField(max_length=30, blank=True)
    cores_per_node = models.IntegerField(default=1)
    number_of_processes = models.IntegerField(default=1)
    queue = models.CharField(max_length=30, blank=True)
    project = models.CharField(max_length=30, blank=True)
    walltime = models.IntegerField(default=10)

    class Meta:
        abstract = True


class DefaultDareBigJobPilot(BaseDareBigJobPilot):
    pass


class DefaultDareBigJobPilotAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'service_url', 'cores_per_node', 'number_of_processes', 'queue', 'project', 'walltime')

admin.site.register(DefaultDareBigJobPilot, DefaultDareBigJobPilotAdmin)


class DareBigJob(BaseDareModel):
    cordination_url = models.CharField(max_length=150, blank=True)
    other_info = models.CharField(max_length=150, blank=True)


class DareBigJobPilot(BaseDareBigJobPilot):
    dare_bigjob = models.ForeignKey('DareBigJob')
    time_started = models.DateTimeField()
    pilot_url = models.CharField(max_length=256, blank=True)

    def get_pilot_info(self):
        pilotdescdict = {'service_url': self.service_url,
                        'queue': self.queue,
                        'walltime': self.walltime,
                        'project': self.project,
                        'working_directory': self.working_directory,
                        'number_of_processes': self.number_of_processes,
                        'cores_per_node': self.cores_per_node
                        }
        for key in pilotdescdict.keys():
            pilotdescdict[key] = str(pilotdescdict[key])
        return pilotdescdict

    def get_stop_start(self):
        if self.status in ['New', 'Stopped', 'Canceled']:
            return True
        return False


class DareBigJobTask(BaseDareModel):
    dare_bigjob = models.ForeignKey('DareBigJob')
    dare_bigjob_pilot = models.ForeignKey('DareBigJobPilot', blank=True, null=True)
    script = models.TextField(blank=True)
    inputfiles = models.CharField(max_length=30, blank=True)
    outputfiles = models.CharField(max_length=30, blank=True)
    cu_url = models.CharField(max_length=256, blank=True)

    def get_stop_start(self):
        if self.status in ['New', 'Stopped', 'Canceled', 'Done']:
            return True
        return False


