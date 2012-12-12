from django.db import models
from django.contrib import admin
from django.conf import settings

import datetime
from django.core.files.storage import FileSystemStorage
import random
import string


class Job(models.Model):
    user = models.ForeignKey('auth.User', null=True, related_name='user_jobs')
    name = models.CharField(max_length=30, blank=True)
    job_type = models.CharField(max_length=30, blank=True)
    detail_status = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    @property
    def parameter_file(self):
        pp = JobInfo.objects.filter(job=self, key='parameter_file')
        if len(pp) > 0:
            return pp[0].value

    @property
    def pilot(self):
        pp = JobInfo.objects.filter(job=self, key='pilot')
        if len(pp) > 0:
            return UserResource.objects.get(id=pp[0].value).name

    @property
    def corecount(self):
        pp = JobInfo.objects.filter(job=self, key='corecount')
        if len(pp) > 0:
            return pp[0].value

    @property
    def walltime(self):
        pp = JobInfo.objects.filter(job=self, key='walltime')
        if len(pp) > 0:
            return pp[0].value

    def __repr__(self):
        return "%s-%s" % (self.id, self.name)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        self.status = 'New'
        super(Job, self).save(*args, **kwargs)


class JobInfo(models.Model):
    description = models.CharField(max_length=200, blank=True)
    key = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)
    job = models.ForeignKey('Job', null=True, related_name='job_info')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def __repr__(self):
        return self.key

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(JobInfo, self).save(*args, **kwargs)


class JobQueue(models.Model):
    qstatus = models.CharField(max_length=200, blank=True)
    jobq_type = models.CharField(max_length=30, blank=True)
    job = models.ForeignKey('Job', null=True, related_name='job_in_queue')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(JobQueue, self).save(*args, **kwargs)


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
    list_display = ('user', 'data_service_url', 'service_url', 'cores_per_node', 'queue', 'modified')

    def save_model(self, *args, **kwargs):
        return super(UserContextAdmin, self).save_model(*args, **kwargs)

admin.site.register(UserResource, UserResourceAdmin)
