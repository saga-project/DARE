from celery.decorators import task
from dare.core.dare_manager import DareManager
from darewap.models import Job
from dare.helpers.cfgparser import CfgWriter
import os
from django.conf import settings


@task
def add_dare_job(job):
    if not hasattr(job, 'id'):
        job = Job.objects.get(id=id)
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

    jb_conf = CfgWriter(conf_file)
    section = {'name': 'main',
            'jobid': job.id,
            'steps': 'step_hello_world_1',
            'webupdate': False,
            'used_pilots': 'localhost_pilot'}
    jb_conf.add_section(section)

    section = {'name': 'localhost_pilot',
               'working_directory': '/tmp/',
                'service_url': 'fork://localhost/',
                'number_of_processes': 1}
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
