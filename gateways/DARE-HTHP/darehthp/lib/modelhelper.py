#contains various job manipulation techniques

#job states

import time
import os
import sys

from sqlalchemy.sql import and_, or_
import darehthp.model as model
import darehthp.model.meta as meta


class JOBSTATES(object):
    UNKNOWN = 0
    NEW = 1
    RUNNING = 2
    DONE = 3
    FAILED = 4

def add_job(userid, desc ="", apptype=""):
    #.first()

    """adds a job to the queue"""
    job_queue = model.job()
    job_queue.status = str(JOBSTATES.UNKNOWN)
    job_queue.userid = str(userid)
    job_queue.description = desc
    job_queue.apptype = apptype

    job_queue.submitted_time = time.asctime()

    meta.Session.add(job_queue)
    meta.Session.commit()

    #to find ID
    njob = meta.Session.query(model.job)
    job = njob.filter(model.job.submitted_time == str(job_queue.submitted_time)).one()

    return job.id


def add_jobinfo(newjobinfo):
    meta.Session.add(newjobinfo)
    meta.Session.commit()

#for generic job
def add_jobmeta(jobid, type, sid=0):

    """adds a job to the jobmeta"""
    job_meta = model.jobmeta()
    job_meta.jobid = str(jobid)
    job_meta.type = str(type)
    job_meta.someid = sid

    job_meta.submitted_time = time.asctime()

    meta.Session.add(job_meta)
    meta.Session.commit()

    #to find ID
    njobmeta = meta.Session.query(model.jobmeta)
    jobmeta = njobmeta.filter(model.jobmeta.submitted_time == str(job_meta.submitted_time)).one()

    return jobmeta.id


def add_jobinfo_new(key, value, jobmetaid):
    newjobinfo = model.jobinfo()
    newjobinfo.key = key
    newjobinfo.value = value
    newjobinfo.jobmetaid = jobmetaid

    newjobinfo.submitted_time = time.asctime()
    meta.Session.add(newjobinfo)
    meta.Session.commit()


def get_jobinfo(jobid):
    #to find ID
    jobinfo = meta.Session.query(model.jobinfo)
    new_jobinfo = jobinfo.filter(model.jobinfo.jobid == jobid)
    return new_jobinfo


def get_jobmeta_jobid(jobmetaid):
    #to find ID
    jobmeta = meta.Session.query(model.jobmeta)
    new_jobinfo = jobmeta.filter(model.jobmeta.id == jobmetaid).one()
    return new_jobinfo.jobid



def get_jobtype(jobid):
    #to find ID
    jobinfo = meta.Session.query(model.jobinfo)
    new_jobinfo = jobinfo.filter(and_(model.jobinfo.jobid ==jobid\
                 , model.jobinfo.key == "appname")).one()

    return new_jobinfo.value



def get_jobinfoids(jobid):
    #to find ID
    jobinfo = meta.Session.query(model.jobinfo)
    new_jobinfo = jobinfo.filter(model.jobinfo.jobid == jobid)
    newjobinfoids =[]
    if (new_jobinfo):
        for jq in new_jobinfo:
            newjobinfoids.append(jq.id)
    else:
        newjobinfoids.append("nojobinfo")

    return newjobinfoids


def get_jobid(jobinfoid):
    #to find ID
    jobinfo = meta.Session.query(model.jobinfo)
    new_jobinfo = jobinfo.filter(model.jobinfo.id == jobinfoid)
    newjobinfoids =[]

    if (new_jobinfo):
        jobid = jq.id
    else:
        jobid= "nojobid"
    return jobid

def del_job(jobid):

    """deletes a job from the jobs"""
    jobs =  meta.Session.query(model.job).get(jobid)
    meta.Session.delete(jobs)

    """deletes a job from job info table"""
    jobinfo = meta.Session.query(model.jobinfo)
    jobsinfo =  jobinfo.filter(model.jobinfo.jobid==jobid).all()
    for deljobsinfo in jobsinfo:
        meta.Session.delete(jobsinfo)
    meta.Session.commit()

def update_job_status(jobid, status):
    """updates a job status from the queue"""
    jobs_q =  meta.Session.query(model.job)
    jq =  jobs_q.filter(model.job.id==jobid).one()
    jq.status = str(status)
    meta.Session.commit()

def update_job_pid(jobid, pid):
    """updates a job status from the queue"""
    jobs_q =  meta.Session.query(model.job)
    jq =  jobs_q.filter(model.job.id==jobid).one()
    print "updating",jobid, pid
    jq.dareprocess_id = str(pid)
    meta.Session.commit()

def get_job_pid(jobid):
    #to find ID
    job= meta.Session.query(model.job)
    new_job = job.filter(model.job.id ==jobid).one()
    pid = new_job.dareprocess_id
    if (pid==""):
        pid = None
    return pid


def update_job_detail_status(jobid, detail_status):
    """updates a job status from the queue"""
    jobs_q =  meta.Session.query(model.job)
    jq =  jobs_q.filter(model.job.id==jobid).one()
    jq.detail_status = str(detail_status)
    meta.Session.commit()


def check_new_jobs():
    jobs =  meta.Session.query(model.job)

  # jobs that are in queue
    new_jobs =  jobs.filter(model.job.status==str(JOBSTATES.NEW)).all()
    newjobids =[]

    if (new_jobs):
        for jq in new_jobs:
            newjobids.append(jq.id)
    else:
        newjobids.append("nojobs")
    print "check new jobs Done",newjobids
    return newjobids

def get_job_pid(jobid):
    #to find ID
    job= meta.Session.query(model.job)
    new_job = job.filter(model.job.id ==jobid).one()
    pid = new_job.dareprocess_id
    if (pid==""):
        pid = None
    return pid


""" absolete
def update_jobinfo_status(jobinfoid, status):
    #updates a job status from the queue
    jobid = get_jobid(jobinfoid)

    #apply statuses here remote queue but running launched
    if (status ==status):
        ustatus = status

    update_job_status(jobid, ustatus)
    jobs_q =  meta.Session.query(model.jobinfo)
    jq =  jobs_q.filter(model.jobinfo.id==jobinfoid).one()
    jq.status = str(status)
    meta.Session.commit()
"""
