from django.db import models


class Job(models.Model):
    status = models.CharField(max_length=30, blank=True)
    submitted_time = models.DateTimeField()
    job_type = models.CharField(max_length=30, blank=True)
    detail_status = models.CharField(max_length=30, blank=True)
    dareprocess_id = models.CharField(max_length=30, blank=True)
    userid = models.ForeignKey('auth.User', null=True, related_name='user_jobs')


class JobInfo(models.Model):
    description = models.CharField(max_length=200, blank=True)
    submitted_time = models.DateTimeField()
    key = models.CharField(max_length=200, blank=True)
    value = models.CharField(max_length=200, blank=True)
    jobid = models.ForeignKey('Job', null=True, related_name='job_info')


class JobQueue(models.Model):
    qstatus = models.CharField(max_length=200, blank=True)
    submitted_time = models.DateTimeField()
    jobq_type = models.CharField(max_length=30, blank=True)
    jobid = models.ForeignKey('Job', null=True, related_name='job_in_queue')
