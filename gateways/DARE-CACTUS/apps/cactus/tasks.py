from celery.decorators import task
from dare.core.dare_manager import DareManager
from darewap.models import Job


@task
def add_dare_job(job_id):
    config_file = create_job_config_file(job_id)
    DareManager(config_file)
    return config_file


def create_job_config_file(job_id):
    pass
