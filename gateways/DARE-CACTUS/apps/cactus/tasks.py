from celery.decorators import task
from dare.core.dare_manager import DareManager
from darewap.models import Job
from dare.helpers.cfgparser import CfgWriter


@task
def add_dare_job(job_id):
    config_file = create_job_config_file(job_id)
    #DareManager(config_file)
    return config_file


def create_job_config_file(jobid):
    conf_file = jobid
    jb_conf = CfgWriter(conf_file)
    section = {'name': 'main',
            'jobid': jobid,
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

    return jb_conf.write()
