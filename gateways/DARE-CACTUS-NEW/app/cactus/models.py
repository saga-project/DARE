from django.db import models
from darewap.models import Job
import datetime


class Thornfiles(models.Model):
    filename = models.CharField(max_length=30, blank=True)
    thornfile = models.FileField(upload_to='thornfiles/%Y/%m/%d')
    description = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey('auth.User', related_name='user_thorns')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Thornfiles, self).save(*args, **kwargs)


class Paramlist(models.Model):
    filename = models.CharField(max_length=30, blank=True)
    paramfile = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=30, blank=True)
    submitted_time = models.DateTimeField()
    job = models.ForeignKey(Job, related_name='job_params')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Paramlist, self).save(*args, **kwargs)

