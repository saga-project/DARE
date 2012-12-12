#!/usr/bin/env python
__author__ = "Sharath Maddineni"
__copyright__ = "Copyright 2011-2012, Sharath Maddineni"
__license__ = "MIT"


import uuid
import time
import threading
from dare import darelogger

from dare.helpers.stepunit import StepUnitStates
from dare.helpers.prepareworkflow import PrepareWorkFlow

from dare.helpers.updater import Updater
from dare import COORDINATION_URL

from pilot import PilotComputeService, PilotDataService, ComputeDataServiceDecentral


class DareManager(object):
    """DARE manager:
       - reads different configuration files
       - submits compute/data units as that in various steps"""

    """Constructor"""
    def __init__(self, conffile="/path/to/conf/file"):
        "" ""
        self.dare_conffile = conffile
        self.workflow = PrepareWorkFlow(self.dare_conffile)
        self.updater = Updater(self.workflow.update_site_db, self.workflow.dare_web_id)
        self.dare_id = "dare-" + str(uuid.uuid1())
        self.data_pilot_service_repo = []
        self.step_threads = {}
        try:
            self.start()
        except KeyboardInterrupt:
            self.quit(message='KeyboardInterrupt')

    def start(self):
        darelogger.info("Creating Compute Engine service ")
        self.pilot_compute_service = PilotComputeService(coordination_url=COORDINATION_URL)
        self.pilot_data_service = PilotDataService(coordination_url=COORDINATION_URL)

        for compute_pilot, desc in self.workflow.compute_pilot_repo.items():
            self.pilot_compute_service.create_pilot(pilot_compute_description=desc)

        for data_pilot, desc in self.workflow.data_pilot_repo.items():
            self.data_pilot_service_repo.append(self.pilot_data_service.create_pilot(pilot_data_description=desc))

        self.compute_data_service = ComputeDataServiceDecentral()
        self.compute_data_service.add_pilot_compute_service(self.pilot_compute_service)
        self.compute_data_service.add_pilot_data_service(self.pilot_data_service)

        ### run the steps
        self.step_start_lock = threading.RLock()
        self.step_run_lock = threading.RLock()

        for step_id in self.workflow.step_units_repo.keys():
                darelogger.info(" Sumitted step %s " % step_id)
                self.step_start_lock.acquire()
                self.start_thread_step_id = step_id
                self.step_start_lock.release()
                self.step_threads[step_id] = threading.Thread(target=self.start_step)
                self.step_threads[step_id].start()

        while(1):
            count_step = [v.is_alive() for k, v in self.step_threads.items()]
            darelogger.info('count_step %s' % count_step)
            if not True in count_step and len(count_step) > 0:
                break
            time.sleep(10)

        darelogger.info(" All Steps Done processing")

        self.quit(message='quit gracefully')

    def check_to_start_step(self, step_id):
        flags = []
        darelogger.info(self.workflow.step_units_repo[step_id].UnitInfo['start_after_steps'])
        if self.workflow.step_units_repo[step_id].get_status() == StepUnitStates.New:
            for dep_step_id in self.workflow.step_units_repo[step_id].UnitInfo['start_after_steps']:
                if self.workflow.step_units_repo[dep_step_id].get_status() != StepUnitStates.Done:
                    flags.append(False)
                darelogger.info(self.workflow.step_units_repo[dep_step_id].get_status())
        return False if False in flags else True

    def start_step(self):
        self.step_start_lock.acquire()
        step_id = self.start_thread_step_id
        self.step_start_lock.release()

        while(1):
            darelogger.info(" Checking to start step %s " % step_id)
            if self.check_to_start_step(step_id):
                self.run_step(step_id)
                break
            else:
                darelogger.info(" Cannot start this step %s sleeping..." % step_id)
                time.sleep(10)

    def run_step(self, step_id):
        #self.step_run_lock.acquire()
        #job started update status
        this_su = self.workflow.step_units_repo[step_id].UnitInfo
        self.updater.update_status(this_su['dare_web_id'], "%s in step %s" % ('Running',  this_su['name']))

        darelogger.info(" Started running %s " % step_id)

        jobs = []
        job_start_times = {}
        job_states = {}
        NUMBER_JOBS = len(self.workflow.step_units_repo[step_id].UnitInfo['compute_units'])
        for cu_id in self.workflow.step_units_repo[step_id].UnitInfo['compute_units']:
            compute_unit_desc = self.workflow.compute_units_repo[cu_id]
            input_dus = compute_unit_desc.pop('input_data_units')
            output_dus = compute_unit_desc.pop('output_data_units')
            input_data_units = []
            for du_id in input_dus:
                input_data_units.append(self.compute_data_service.submit_data_unit(self.workflow.data_units_repo[du_id]))
            output_data_units = []
            for du_id in output_dus:
                output_data_units.append(self.compute_data_service.submit_data_unit(self.workflow.data_units_repo[du_id]))

            compute_unit_desc["input_data"] = [du.get_url() for du in input_data_units]
            compute_unit_desc["output_data"] = [{du.get_url(): ['std*']} for du in output_data_units]
            compute_unit = self.compute_data_service.submit_compute_unit(compute_unit_desc)

            darelogger.info("Compute Unit: Description: \n%s" % (str(self.workflow.compute_units_repo[cu_id])))
            jobs.append(compute_unit)
            job_start_times[compute_unit] = time.time()
            job_states[compute_unit] = compute_unit.get_state()

        darelogger.debug("************************ All Jobs submitted ************************")

        while 1:
            finish_counter = 0
            result_map = {}
            for i in range(0, NUMBER_JOBS):
                old_state = job_states[jobs[i]]
                state = jobs[i].get_state()
                if  state in result_map == False:
                    result_map[state] = 0
                result_map[state] = result_map.get(state, 0) + 1
                #print "counter: " + str(i) + " job: " + str(jobs[i]) + " state: " + state
                if old_state != state:
                    darelogger.debug("Job " + str(jobs[i]) + " changed from: " + old_state + " to " + state)
                if old_state != state and self.has_finished(state) == True:
                    darelogger.info("%s step Job: " % (self.workflow.step_units_repo[step_id].UnitInfo['name']) + str(jobs[i]) + " Runtime: " + str(time.time() - job_start_times[jobs[i]]) + " s.")
                if self.has_finished(state) == True:
                    finish_counter = finish_counter + 1
                job_states[jobs[i]] = state

            darelogger.debug("Current states: " + str(result_map))
            time.sleep(5)
            if finish_counter == NUMBER_JOBS:
                break

        self.workflow.step_units_repo[step_id].set_status(StepUnitStates.Done)

        #self.compute_data_service.wait()
        darelogger.debug(" Compute jobs for step %s complete" % step_id)

        #runtime = time.time()-starttime

        #all jobs done update status
        self.updater.update_status(this_su['dare_web_id'], "%s is Done" % this_su['name'])

        #self.step_run_lock.release()

    def has_finished(self, state):
        state = state.lower()
        if state == "done" or state == "failed" or state == "canceled":
            return True
        else:
            return False

    def quit(self, message=None):
        if message:
            darelogger.debug(message)
        darelogger.debug("Terminating steps")
        for step, thread  in self.step_threads.items():
            darelogger.debug("Stoppping step %s" % step)
            thread._Thread__stop()

        darelogger.debug("Terminating Pilot Compute/Data Service")
        try:
            self.compute_data_service.cancel()
            self.pilot_data_service.cancel()
            self.pilot_compute_service.cancel()
        except:
            pass
