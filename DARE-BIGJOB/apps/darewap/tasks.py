from celery.decorators import task
import saga
import getpass

from .models import DareBigJobPilot, DareBigJobTask
from RestrictedPython import compile_restricted
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import safe_builtins, full_write_guard
from pilot import PilotComputeService, PilotCompute, ComputeUnit, State

COORD_URL = "redis://cyder.cct.lsu.edu:2525/"

DEFAULT_CUD = {"executable": "/bin/date",
                "arguments": [''],
                "total_core_count": 1,
                "number_of_processes": 1,
                "output": "stdout.txt",
                "error": "stderr.txt",
              }


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

CONDOR_URL = "condor://localhost?WhenToTransferOutput=ON_EXIT&should_transfer_files=YES&notification=Always"


@task
def start_run_osg_task(task_id):

    # Your ssh identity on the remote machine.
    ctx = saga.Context("ssh")
    ctx.user_id = getpass.getuser()  # Change if necessary

    session = saga.Session()
    session.add_context(ctx)

    js = saga.job.Service(CONDOR_URL, session=session)

    jd = saga.job.Description()

    jd.name = 'testjob'
    jd.project = 'TG-MCB090174'
    jd.environment = {'RUNTIME': '/etc/passwd'}
    jd.wall_time_limit = 2  # minutes

    jd.executable = '/bin/cat'
    jd.arguments = ["$RUNTIME"]

    jd.output = "saga_condorjob.stdout"
    jd.error = "saga_condorjob.stderr"

#       jd.candidate_hosts = ["FNAL_FERMIGRID", "cinvestav", "SPRACE",
#                             "NYSGRID_CORNELL_NYS1", "Purdue-Steele",
#                             "MIT_CMS_CE2", "SWT2_CPB", "AGLT2_CE_2",
#                             "UTA_SWT2", "GridUNESP_CENTRAL",
#                             "USCMS-FNAL-WC1-CE3"]

    # create the job (state: New)
    sleepjob = js.create_job(jd)

    # check our job's id and state
    print "Job ID    : %s" % (sleepjob.id)
    print "Job State : %s" % (sleepjob.state)

    print "\n...starting job...\n"
    sleepjob.run()

    print "Job ID    : %s" % (sleepjob.id)
    print "Job State : %s" % (sleepjob.state)


def get_osg_task_status(task_id):

    # Your ssh identity on the remote machine.
    ctx = saga.Context("ssh")
    ctx.user_id = getpass.getuser()  # Change if necessary

    session = saga.Session()
    session.add_context(ctx)

    js = saga.job.Service(CONDOR_URL, session=session)

    sleebjob_clone = js.get_job(task_id)
    return sleebjob_clone.state
