#!/usr/bin/env python
__author__ = "Sharath Maddineni"
__copyright_ = "Copyright 2011-2012, Sharath Maddineni"
__license__ = "MIT"

import uuid
import sys

from .misc import darelogger
from .stepunit import StepUnit, StepUnitStates
from .cfgparser import CfgParser


class PrepareWorkFlow(object):
    """DARE prepare WF:
       - reads different configuration files
       - creates work flow, pilot units, step units, compute units, data units."""

    """Constructor"""
    def __init__(self, conffile):
        "" ""
        self.dare_conffile = conffile
        self.dare_id = "dare-" + str(uuid.uuid1())
        self.darecfg = {}
        self.compute_pilot_repo = {}
        self.data_pilot_repo = {}
        self.step_units_repo = {}
        self.compute_units_repo = {}
        self.data_units_repo = {}

        self.create_static_workflow()

    def process_config_file(self):

        self.dare_conf_full = CfgParser(self.dare_conffile)
        self.dare_conf_main = self.dare_conf_full.SectionDict('main')
        self.update_site_db = self.dare_conf_main.get('update_web_db', False)
        self.dare_web_id = self.dare_conf_main.get('web_id', False)

    def create_static_workflow(self):
        self.process_config_file()
        darelogger.info("Done Reading DARE Config File")

        self.prepare_pilot_units()

        self.prepare_step_units()
        self.prepare_compute_units()

    def prepare_pilot_units(self):
        darelogger.info("Starting to prepare pilot Units")

        for pilot in self.dare_conf_main['used_pilots'].split(','):
            pilot = pilot.strip()
            compute_pilot_uuid = "compute-pilot-%s-%s" % (pilot, str(uuid.uuid1()))
            data_pilot_uuid = "compute-pilot-%s-%s" % (pilot, str(uuid.uuid1()))

            pilot_compute_description = {}

            try:
                pilot_compute_description = self.dare_conf_full.SectionDict(pilot)
            except:
                error = "Cannot find section for Pilot %s" % pilot
                darelogger.error(error)
                raise RuntimeError(error)

            pilot_compute_description['number_of_processes'] = int(pilot_compute_description.get('number_of_processes', 1))
            pilot_compute_description['walltime'] = int(pilot_compute_description.get('number_of_processes', 100))

            # create pilot job service and initiate a pilot job
            pilot_compute_description.update({'affinity_datacenter_label': '%s-adl' % pilot,
                            'affinity_machine_label': '%s-aml' % pilot,
                            })

            self.compute_pilot_repo[compute_pilot_uuid] = pilot_compute_description

            if pilot_compute_description.get('data_service_url'):
                pilot_data_description = {
                                    "service_url": pilot_compute_description.pop('data_service_url'),
                                    "size": 100,
                                    "affinity_datacenter_label": pilot + '-dcl',
                                    "affinity_machine_label": pilot + '-aml'
                                 }

                self.data_pilot_repo[data_pilot_uuid] = pilot_data_description

        darelogger.info("Done preparing Pilot Units ")

    def prepare_step_units(self):
        darelogger.info("Starting to prepare Step Units ")

        #TODO:: check for same names

        for step in self.dare_conf_main['steps'].split(','):
            darelogger.info("Preparing Step Units: %s" % step)
            step_info = {}
            try:
                step_info = self.dare_conf_full.SectionDict(step.strip())
            except:
                error = "step description section not found for step %s" % step
                darelogger.error(error)
                raise RuntimeError(error)

            start_after_steps = []

            if step_info.get('start_after_steps'):
                start_after_steps = ["%s-%s" % (k.strip(), self.dare_id) for k in step_info.get('start_after_steps').split(',')]

            step_unit_uuid = "%s-%s" % (step.strip(), self.dare_id)
            step_info.update({
                      "name": step.strip(),
                      "step_id": step_unit_uuid,
                      "dare_web_id": self.dare_web_id,
                      "status": StepUnitStates.New,
                      "start_after_steps": start_after_steps,
                      "compute_units": [],
                      "transfer_input_data_units": [],
                      "transfer_output_data_units": []
                      })

            su = StepUnit()
            su.define_param(step_info)
            self.step_units_repo[step_unit_uuid] = su

        darelogger.info("Done preparing Step Units ")

    def prepare_compute_units(self):
        """add prepare work dir """

        darelogger.info("Starting to prepare Compute Units ")

        for step in self.dare_conf_main['steps'].split(','):
            darelogger.info("Preparing compute Units: %s" % step)

            try:
                step_info = self.dare_conf_full.SectionDict(step.strip())
            except:
                error = "step description section not found for step %s" % step
                darelogger.error(error)
                raise RuntimeError(error)

            for cu in step_info.get('compute_units', '').split(','):
                cu = cu.strip()
                compute_unit_description = {}
                try:
                    compute_unit_description = self.dare_conf_full.SectionDict(cu.strip())
                except:
                    error = "section not found for compute unit %s" % cu
                    darelogger.error(error)
                    raise RuntimeError(error)

                cu_uuid = "cu-%s" % (uuid.uuid1(),)
                cu_step_id = "%s-%s" % (step.strip(), self.dare_id)

                pilot = compute_unit_description.get('pilot', self.dare_conf_main['used_pilots'].split(',')[0]).strip()
                compute_unit_description['arguments'] = [compute_unit_description.get('arguments')]
                compute_unit_description.update({"output": "dare-cu-stdout-" + cu_uuid + ".txt",
                                                "error": "dare-cu-stderr-" + cu_uuid + ".txt",
                                                "affinity_datacenter_label": "%s-adl" % pilot,
                                                "affinity_machine_label": "%s-aml" % pilot})

                compute_unit_description['input_data_units'] = []
                if compute_unit_description.get('transfer_input_data'):
                    files = compute_unit_description.pop('transfer_input_data').split(',')
                    compute_unit_description['input_data_units'].append(self.prepare_data_unit(files, pilot))

                compute_unit_description['output_data_units'] = []
                if compute_unit_description.get('transfer_output_data'):
                    files = compute_unit_description.pop('transfer_output_data')
                    compute_unit_description['output_data_units'].append(self.prepare_data_unit(files, pilot))
                self.compute_units_repo[cu_uuid] = compute_unit_description
                self.step_units_repo[cu_step_id].add_cu(cu_uuid)

        darelogger.info("Done preparing compute Units ")

    def prepare_data_unit(self, files, pilot):
        du_uuid = "du-%s" % (uuid.uuid1(),)
        data_unit_description = {"file_urls": files,
                                "affinity_datacenter_label": "%s-adl" % pilot,
                                "affinity_machine_label": "%s-aml" % pilot}
        self.data_units_repo[du_uuid] = data_unit_description
        return du_uuid

    def __repr__(self):
        return  self.dare_id
