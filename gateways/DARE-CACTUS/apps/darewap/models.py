from django.db import models
from django.contrib import admin
from django.conf import settings

import datetime
from django.core.files.storage import FileSystemStorage
import random
import string


class Job(models.Model):
    status = models.CharField(max_length=30, blank=True)
    job_type = models.CharField(max_length=30, blank=True)
    detail_status = models.CharField(max_length=30, blank=True)
    dareprocess_id = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey('auth.User', null=True, related_name='user_jobs')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def __repr__(self):
        return "%s-%s" % (self.id, self.type)

    @property
    def app_type(self):
        return JobInfo.objects.filter(id=self.id).filter(key='app_type')

    @property
    def status(self):
        return JobInfo.objects.filter(id=self.id).filter(key='status')

    @property
    def description(self):
        return JobInfo.objects.filter(id=self.id).filter(key='description')

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
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


class UserContext(models.Model):
    '''  saga.Context() properties'''
    user = models.ForeignKey('auth.User', null=True, related_name='user_context')
    type = models.CharField(max_length=30, blank=True)
    usercert = models.FileField(upload_to=get_usercert, storage=fs)
    userproxy = models.FileField(upload_to=get_userproxy, storage=fs)
    userid = models.CharField(max_length=30, blank=True)
    userkey = models.CharField(max_length=30, blank=True)
    userpass = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

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
