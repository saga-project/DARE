from celery.decorators import task
from dare.core.dare_manager import DareManager
from darewap.models import Job, JobInfo, UserResource, UserTasks
from dare.helpers.cfgparser import CfgWriter
import os
from django.conf import settings
from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import safe_builtins, full_write_guard
import simplejson as json
from pilot import PilotComputeService, PilotCompute, ComputeUnit, State
BIGJOB_DIRECTORY = "~/.bigjob/"

COORD_URL = "redis://cyder.cct.lsu.edu:2525/"

DEFAULT_CUD = {
                    "executable": "/bin/date",
                    "arguments": [''],
                    "total_core_count": 1,
                    "number_of_processes": 1,
                    "output": "stdout.txt",
                    "error": "stderr.txt",
                }


@task
def start_pilot(job_id, pilot_id, coordination_url=COORD_URL):
    job = Job.objects.get(id=job_id)
    jbinfo = job.get_or_create_jobinfo_for_pilot(pilot_id)
    pilot_compute_description = json.loads(jbinfo.user_pilot.detail)
    pilot_compute_service = PilotComputeService(coordination_url=COORD_URL)
    pilot_compute = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    pilot_url = pilot_compute.get_url()
    jbinfo.detail['pilot_url'] = pilot_url
    jbinfo.detail['status'] = "Submitted"
    jbinfo.save()
    print("Started Pilot: %s" % (pilot_url))


@task
def stop_pilot(job_id, pilot_id, coordination_url=COORD_URL):

    job = Job.objects.get(id=job_id)
    pilot = job.get_or_create_jobinfo_for_pilot(pilot_id)
    print pilot.detail
    pilot_url = pilot.detail.get("pilot_url")
    #cancle
    pilot_compute = PilotCompute(pilot_url=pilot_url)
    pilot_compute.cancel()

    pilot.detail['pilot_url'] = ""
    pilot.detail['status'] = "Stopped"
    pilot.save()
    print("Started Pilot: %s" % (pilot_url))


@task
def get_pilot_status(job_id, pilot_id, coordination_url=COORD_URL):

    job = Job.objects.get(id=job_id)
    pilot = job.get_or_create_jobinfo_for_pilot(pilot_id)
    pilot_url = pilot.detail.get("pilot_url")

    if pilot_url:
        pilot_compute = PilotCompute(pilot_url=pilot_url)

        if pilot.detail.get('status') == "Submitted":
            print pilot.detail.get('status')
            if pilot_compute.get_state() == State.Running:
                status = "Running"
                percentage = 100

            if pilot_compute.get_state() == State.New:
                status = "New"
                percentage = 0

            if pilot_compute.get_state() == State.Unknown:
                status = "Submitted"
                percentage = 30

        else:
            percentage = 0
            status = ""

        print pilot.detail['status'], percentage, status
        p = {'ur_id': pilot_id, 'percentage': percentage, 'state': status}
        return p
    else:
        if pilot.detail.get('status') == "Stopped":
            return {'ur_id': pilot_id, 'percentage': 0, 'state': "Stopped"}
        else:
            return {'ur_id': pilot_id, 'percentage': 0, 'state': State.Unknown}


@task
def start_task(staskid):

    taskinfo = JobInfo.objects.get(id=int(staskid))
    if hasattr(taskinfo, 'job_pilot_id'):
        #job_pilot_id = taskinfo.detail.job_pilot_id
        pass

    for pilot in JobInfo.objects.filter(job=taskinfo.job, itype='pilot'):
        pilot_url = pilot.detail['pilot_url']
        pilot_compute = PilotCompute(pilot_url=pilot_url)
        if pilot_compute.get_state() == State.Running:
            break

    if pilot_url:
        ut = taskinfo.user_task
        code = compile_restricted(ut.script, '<string>', 'exec')
        restricted_globals = dict(__builtins__=safe_builtins)
        _print_ = PrintCollector
        _write_ = full_write_guard
        _getattr_ = getattr
        global _getiter_, _getattr_, _write_, _print_, restricted_globals
        _getiter_ = list
        exec(code)
        cus = tasks()
        if pilot_url:
            pilot_compute = PilotCompute(pilot_url=pilot_url)
            for cu in cus:
                compute_unit = pilot_compute.submit_compute_unit(cu)
                print "Started ComputeUnit: %s" % (compute_unit.get_url())
                taskinfo.detail['cu_url'] = compute_unit.get_url()
                taskinfo.detail['status'] = 'Submitted'
                taskinfo.save()
            return compute_unit
        #except:
        #    pass

@task
def get_task_status(staskid):

    taskinfo = JobInfo.objects.get(id=int(staskid))
    cu_url = taskinfo.detail.get('cu_url')
    percentage = taskinfo.detail.get('percentage', 0)
    status = taskinfo.detail['status']

    if cu_url:
        compute_unit = ComputeUnit(cu_url=cu_url)
        if compute_unit.get_state() == State.Running:
            status = "Running"
            percentage = 50

        elif compute_unit.get_state() == State.Done:
            status = State.Done
            percentage = 100
        else:
            if taskinfo.detail.get('status') == "Submitted":
                percentage = 20
                status = "Submitted"

        taskinfo.detail['status'] = status
        taskinfo.detail['percentage'] = percentage
        taskinfo.save()

    return {'staskid': staskid, 'percentage': percentage, 'state': status}


"""
    #pilot_compute_description = pilot.detail

    #pilot_compute_description.update({"number_of_processes": 1,
    #                     "processes_per_node": 1,
    #                     "walltime": 16,
    #                     "project": "TG-MCB090174",
    #                     })
    #pilot_compute_description = dict([(k, str(v)) for k, v in pilot_compute_description.items()])

    #import pdb;pdb.set_trace()

        pilot_compute_description = {"service_url": "fork://localhost",
                         "number_of_processes": 1,
                         "working_directory":  '/tmp/',
                         "number_of_processes": 1,
                         "processes_per_node": 1}
"""
