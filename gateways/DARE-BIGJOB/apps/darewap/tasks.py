from celery.decorators import task
from dare.core.dare_manager import DareManager
from darewap.models import Job, JobInfo, UserResource
from dare.helpers.cfgparser import CfgWriter
import os
from django.conf import settings

import bigjob
from pilot import PilotComputeService, PilotCompute, ComputeUnit, State
BIGJOB_DIRECTORY = "~/.bigjob/"


@task
def start_pilot(job_id, ur_id, coordination_url="redis://cyder.cct.lsu.edu:2525/"):

    job = Job.objects.get(id=job_id)
    pilot = job.get_pilot_with_ur(ur_id)
    print pilot.detail
    # create pilot job service and initiate a pilot job
    pilot_compute_description = {"service_url": "fork://localhost",
                         "number_of_processes": 1,
                         "working_directory":  '/tmp/',
                         "number_of_processes": 1,
                         "processes_per_node": 1}

    pilot_compute_service = PilotComputeService(coordination_url=coordination_url)
    pilot_compute = pilot_compute_service.create_pilot(pilot_compute_description=pilot_compute_description)
    pilot_url = pilot_compute.get_url()
    pilot.detail['pilot_url'] = pilot_url
    pilot.detail['status'] = "Submitted"
    pilot.save()
    print("Started Pilot: %s" % (pilot_url))


@task
def stop_pilot(job_id, ur_id, coordination_url="redis://cyder.cct.lsu.edu:2525/"):

    job = Job.objects.get(id=job_id)
    pilot = job.get_pilot_with_ur(ur_id)
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
def get_pilot_status(job_id, ur_id, coordination_url="redis://cyder.cct.lsu.edu:2525/"):

    job = Job.objects.get(id=job_id)
    pilot = job.get_pilot_with_ur(ur_id)
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
        p = {'ur_id': ur_id, 'percentage': percentage, 'state': status}
        return p
    else:
        if pilot.detail.get('status') == "Stopped":
            return {'ur_id': ur_id, 'percentage': 0, 'state': "Stopped"}
        else:
            return {'ur_id': ur_id, 'percentage': 0, 'state': State.Unknown}


