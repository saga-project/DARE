from django.db import models
from darewap.models import Job
import datetime


class Thornfiles(models.Model):
    name = models.CharField(max_length=30, blank=True)
    thornfile = models.FileField(upload_to='thornfiles/%Y/%m/%d')
    description = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey('auth.User', related_name='user_thorns')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def __unicode__(self):
        return self.thornfile.name 

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        super(Thornfiles, self).save(*args, **kwargs)


class Paramfiles(models.Model):
    filename = models.CharField(max_length=30, blank=True)
    paramfile = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=30, blank=True)
    job = models.ForeignKey(Job, related_name='job_params')
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def __unicode__(self):
        return self.paramfile.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Paramfiles, self).save(*args, **kwargs)
