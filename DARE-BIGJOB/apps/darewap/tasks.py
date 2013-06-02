from celery.decorators import task

from .models import Job, JobInfo, DareBigJob, DareBigJobPilot, DareBigJobTask
from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import safe_builtins, full_write_guard
#from sandbox import Sandbox
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
    jbinfo.detail['status'] = "Submitted"
    jbinfo.save()
    pilot_compute_description = json.loads(jbinfo.user_pilot.detail)
    pilot_compute_service = PilotComputeService(coordination_url=COORD_URL)
    pilot_compute = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    pilot_url = pilot_compute.get_url()
    jbinfo.detail['pilot_url'] = pilot_url
    jbinfo.save()
    print("Started Pilot: %s" % (jbinfo.detail['pilot_url']), jbinfo.id)


@task
def stop_pilot(job_id, pilot_id, coordination_url=COORD_URL):

    job = Job.objects.get(id=job_id)
    pilot = job.get_or_create_jobinfo_for_pilot(pilot_id)
    print pilot.detail
    pilot_url = pilot.detail.get("pilot_url")
    #cancle
    #try:
    pilot_compute = PilotCompute(pilot_url=pilot_url)
    pilot_compute.cancel()
    pilot.detail['pilot_url'] = ""
    pilot.detail['status'] = "Stopped"
    pilot.save()
    #except:
    #    pass

    print("Stopped Pilot: %s" % (pilot_url))


@task
def get_pilot_status(job_id, pilot_id, coordination_url=COORD_URL):

    job = Job.objects.get(id=job_id)
    pilot = job.get_or_create_jobinfo_for_pilot(pilot_id)
    pilot_url = pilot.detail.get("pilot_url")

    if pilot_url:
        try:
            pilot_compute = PilotCompute(pilot_url=pilot_url)
        except:
            pilot.detail['status'] = "Stopped"
            pilot.save()
        if pilot.detail.get('status') == "Submitted":
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
        elif pilot.detail.get('status') == "Submitted":
            return {'ur_id': pilot_id, 'percentage': 30, 'state': "Submitted"}
        else:
            return {'ur_id': pilot_id, 'percentage': 0, 'state': State.Unknown}


@task
def start_task(staskid):

    taskinfo = JobInfo.objects.get(id=int(staskid))
    if hasattr(taskinfo, 'job_pilot_id'):
        #job_pilot_id = taskinfo.detail.job_pilot_id
        pass

    pilot_url = None
    for pilot in JobInfo.objects.filter(job=taskinfo.job, itype='pilot'):
        print pilot.id
        #import pdb;pdb.set_trace()
        if pilot.detail.get('pilot_url'):
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


@task
def start_run_pilot(pilot_id, coordination_url=COORD_URL):
    pilot = DareBigJobPilot.objects.get(id=pilot_id)
    pilot_compute_service = PilotComputeService(coordination_url=COORD_URL)
    print pilot.get_pilot_info()
    pilot_compute = pilot_compute_service.create_pilot(pilot_compute_description=pilot.get_pilot_info())
    pilot.pilot_url = pilot_compute.get_url()
    pilot.status = "Submitted"
    pilot.save()
    print("Started Pilot: %s " % (pilot.pilot_url), pilot.id)


@task
def update_status_run_pilot(pilot_id):

    pilot = DareBigJobPilot.objects.get(id=pilot_id)
    pilot_url = pilot.pilot_url
    if len(pilot_url) > 0:
        pilot_compute = PilotCompute(pilot_url=str(pilot.pilot_url))
        if pilot_compute.get_state() in [State.Done]:
            pilot.status = "Stopped"
        elif pilot_compute.get_state() in [State.New, State.Unknown]:
            pilot.status = "Submitted"
        elif pilot_compute.get_state() in [State.Running]:
            pilot.status = "Active"
    else:
        if not pilot.status == "Stopped":
            pilot.status = "New"

    pilot.save()
    print("Stopped Pilot: %s " % (pilot_url), pilot.id)


@task
def stop_run_pilot(pilot_id):

    pilot = DareBigJobPilot.objects.get(id=pilot_id)
    pilot_url = pilot.pilot_url
    pilot_compute = PilotCompute(pilot_url=str(pilot.pilot_url))
    pilot_compute.cancel()
    pilot.pilot_url = ""
    pilot.status = "Stopped"
    pilot.save()

    print("Stopped Pilot: %s " % (pilot_url), pilot.id)


@task
def start_run_task(task_id):

    taskinfo = DareBigJobTask.objects.get(id=task_id)
    if len(taskinfo.dare_bigjob_pilot.pilot_url) > 0:
        code = compile_restricted(taskinfo.script, '<string>', 'exec')
        restricted_globals = dict(__builtins__=safe_builtins)
        _print_ = PrintCollector
        _write_ = full_write_guard
        _getattr_ = getattr
        global _getiter_, _getattr_, _write_, _print_, restricted_globals
        _getiter_ = list
        exec(code)
        cus = tasks()
        pilot_compute = PilotCompute(pilot_url=str(taskinfo.dare_bigjob_pilot.pilot_url))
        taskinfo.cu_url = ''
        for cu in cus:
            compute_unit = pilot_compute.submit_compute_unit(cu)
            print "Started ComputeUnit: %s" % (compute_unit.get_url())
            taskinfo.cu_url += '@@@' + compute_unit.get_url()
        taskinfo.status = 'Submitted'
        taskinfo.save()
        return compute_unit


@task
def stop_run_task(task_id):

    taskinfo = DareBigJobTask.objects.get(id=task_id)

    for cu_url in taskinfo.cu_url.split('@@@'):
        if len(cu_url) > 0:
            compute_unit = ComputeUnit(cu_url=str(cu_url))
            compute_unit.cancel()
            print(compute_unit.get_state())
    taskinfo.cu_url = ""
    taskinfo.status = "Stopped"
    taskinfo.save()

    print("Stopped Task: ", taskinfo.id)


@task
def update_status_run_task(task_id):

    taskinfo = DareBigJobTask.objects.get(id=task_id)
    all_status = 'New'
    for cu_url in taskinfo.cu_url.split('@@@'):
        if len(cu_url) > 0:
            compute_unit = ComputeUnit(cu_url=str(cu_url))
            if compute_unit.get_state() in [State.Done]:
                all_status = "Done"
            elif compute_unit.get_state() in [State.New, State.Unknown]:
                all_status = "Submitted"
            elif compute_unit.get_state() in [State.Running]:
                all_status = "Running"

        elif  taskinfo.status == "Stopped":
            all_status = "Stopped"

    taskinfo.status = all_status
    taskinfo.save()
    print("Updated Status Task: ", task_id)
