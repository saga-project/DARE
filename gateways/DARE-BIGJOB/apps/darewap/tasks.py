from celery.decorators import task
from dare.core.dare_manager import DareManager
from darewap.models import Job, JobInfo, UserResource
from dare.helpers.cfgparser import CfgWriter
import os
from django.conf import settings

import bigjob
from pilot import PilotComputeService, PilotCompute, ComputeUnit, State
BIGJOB_DIRECTORY="~/.bigjob/" 


@task
def add_dare_job(job):
    if not hasattr(job, 'id'):
        job = Job.objects.get(id=job)
    config_file = create_job_config_file(job)
    if config_file:
        DareManager(config_file)
        return True
    return False


@task
def get_pilot_status(job):
    if not hasattr(job, 'id'):
        job = Job.objects.get(id=job)
    config_file = create_job_config_file(job)
    if config_file:
        DareManager(config_file)
        return True
    return False


@task
def submit_tasks(job):
    if not hasattr(job, 'id'):
        job = Job.objects.get(id=job)
    config_file = create_job_config_file(job)
    if config_file:
        DareManager(config_file)
        return True
    return False


@task
def get_task_status(job):
    if not hasattr(job, 'id'):
        job = Job.objects.get(id=job)
    config_file = create_job_config_file(job)
    if config_file:
        DareManager(config_file)
        return True
    return False


def create_job_config_file(job):
    directory = os.path.join(str(settings.DARE_JOB_DIR), str(job.id))
    if not os.path.exists(directory):
        os.makedirs(directory)
    conf_file = os.path.join(directory, "%s.dare" % job.id)

    pilot_id = JobInfo.objects.filter(job_id=job.id, key='pilot')[0].value
    number_of_processes = JobInfo.objects.filter(job_id=job.id, key='corecount')[0].value
    pilot_info = UserResource.objects.get(id=pilot_id)
    jb_conf = CfgWriter(conf_file)
    section = {'name': 'main',
            'jobid': job.id,
            'steps': 'step_hello_world_1',
            'webupdate': True,
            'used_pilots': '%s_pilot' % pilot_info.name}
    jb_conf.add_section(section)

    section = {'name': '%s_pilot' % pilot_info.name,
               'working_directory': pilot_info.working_directory,
                'service_url': pilot_info.service_url,
                'data_service_url': pilot_info.data_service_url,
                'cores_per_node': pilot_info.cores_per_node,
                'queue': pilot_info.queue,
                'allocation': pilot_info.allocation,
                'number_of_processes': number_of_processes}
    jb_conf.add_section(section)

    section = {'name': 'step_hello_world_1',
               'cu_type': 'echo_hello_cu',
               'input_args': 'hello_world_one, hello_world_two, hello_world_three',
               'number_of_processes': 1}
    jb_conf.add_section(section)

    section = {'name': 'echo_hello_cu',
               'executable': '/bin/echo',
               'input_args': 'hello_world_one, hello_world_two, hello_world_three'}
    jb_conf.add_section(section)

    if jb_conf.write():
        return conf_file
    return False


@task
def start_pilot(pilot_compute_description, coordination_url="redis://localhost/"):

    # create pilot job service and initiate a pilot job
    pilot_compute_description = {"service_url": "fork://localhost",
                         "number_of_processes": 1,
                         "working_directory":  '/tmp/',
                         "number_of_processes": 1,
                         "processes_per_node": 1}

    pilot_compute_service = PilotComputeService(coordination_url=coordination_url)
    pilot_compute = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    pilot_url = pilot_compute.get_url()

    print("Started Pilot: %s" % (pilot_url))
