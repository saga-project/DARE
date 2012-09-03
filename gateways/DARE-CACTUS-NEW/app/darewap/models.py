from django.db import models
import datetime


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