#Author Sharath Maddineni
"""
A tool to run applications in Distributed environments
depends on Bigjob Troy and local file trasfer mechanisms like
"""

#!/usr/bin/env python
import sys
import os
import time
import pdb
import traceback
import logging

import ConfigParser


if os.getenv("DARENGS_HOME")!=None:
    DARENG_HOME= os.getenv("DARENGS_HOME")
else:
    DARENGS_HOME = os.path.abspath(os.path.join(os.path.abspath(__file__),"..", "..", "..", ".."))
print "DARENGS_HOME", DARENGS_HOME
sys.path.insert(0,DARENGS_HOME)
sys.path.insert(0,BIGJOB_HOME)

try:
    import darengs.lib.ModelConnector as jobmodel_helper
    load_update_env = "true"
except:
    load_update_env = "false"
print "load_update_env", load_update_env


#add bigjob path
if os.getenv("BIGJOB_HOME")!=None:
    BIGJOB_HOME= os.getenv("BIGJOB_HOME")
else:
    BIGJOB_HOME = "~/.bigjob"

try:
    import many_job
except ImportError:
    print "failed to import bigjob"
    sys.exit()

try:
    import saga
except ImportError:
    print "failed to import saga"
    sys.exit()




def dict_section(config, section):

    lst = config.items(section)
    dct={}
    for i in range(len(lst)):
        dct[lst[i][0]]=lst[i][1]
    return dct

class dare(object):

    def __init__(self,conf_file):

        self.jobs = []
        self.job_start_times = {}
        self.job_states = {}

        #parse job conf file
        self.config = ConfigParser.ConfigParser()
        self.config.read(conf_file)

        self.job_conf = dict_section(self.config, "DAREJOB")
        self.load_update_env = load_update_env

    def run(self):

        #create a logfile
        LOG_FILENAME = self.job_conf["log_filename"]
        print LOG_FILENAME
        self.logger = logging.getLogger('dare_multijob')
        hdlr = logging.FileHandler(LOG_FILENAME)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

        #first info in log file
        self.logger.info("Job id  is "+ self.job_conf["jobid"]  )
        self.logger.info("RESOURCES used are " + self.job_conf["num_resources"] )

        try:
            #get resource info
            #start the big job agents
            resource_list = []
            self.mjs = []
            for i in range(0, int(self.job_conf["num_resources"])):
                resource_list.append([])
                resource_list[i].append(dict_section(self.config,"resource_"+ str(i) ))
                #create multiple manyjobs
                print "Create manyjob service "
                self.mjs.append(many_job.many_job_service(resource_list[i], None))
            total_number_of_jobs=0


            ### run the step
            wus_count = 0
            for STEP in range(0, int(self.job_conf["num_steps"])):
                starttime = time.time()

                #job started update status
                if (self.load_update_env == "true"):
                    jobmodel_helper.update_job_detail_status(self.job_conf["jobid"], "In step " + str(STEP +1))

                step_wus = self.job_conf["step_" + str(STEP)].split(',')
                if ("step_" + str(STEP)) not in self.job_conf["ft_steps"].split(','):
                    ### submit the each step wus to bigjob
                    for wu_count in range(0, len(step_wus)):
                         wu = dict_section(self.config, step_wus[wu_count].strip())
                         wus_count = wus_count +1
                         self.submit_wu(wu)
                    self.wait_for_wus(wus_count)
                else:
                    #time.sleep(10)
                    for wu_count in range(0, len(step_wus)):
                         fs = dict_section(self.config, step_wus[wu_count].strip())
                         self.submit_fs(fs)

                runtime = time.time()-starttime

                self.logger.info("STEP"+str(STEP)+" Runtime: " + str(runtime) )

            #all jobs done update status
            if (self.load_update_env == "true"):
                jobmodel_helper.update_job_detail_status(self.job_conf["jobid"], "")
                jobmodel_helper.update_job_status(self.job_conf["jobid"], 4)

            for i in range(0,int(self.job_conf["num_resources"])):
                self.mjs[i].cancel()

        except:
            traceback.print_exc(file=sys.stdout)
            try:
                for i in range(0,int(self.job_conf["num_resources"])):
                    self.mjs[i].cancel()
            except:
                sys.exit()



    def has_finished(self,state):
            state = state.lower()
            if state=="done" or state=="failed" or state=="canceled":
                return True
            else:
                return False

    # file stager for grids and clouds
    #TODO: should be SAGA based and pilot store
    def submit_fs(self,fs):

        source_url=fs["source_url"]
        dest_url=fs["dest_url"]

        self.logger.info( "Now I am tranferring the files from %s to %s"%(source_url, dest_url))
        #fgeuca for clouds
        if (fs["fs_type"] == "fgeuca"):
            try:
                #for cloud files
                cmd = "scp  -r -i /path/to/smaddi2.private %s %s"%(source_url, dest_url)
                os.system(cmd)
            except saga.exception, e:
                error_msg = "File stage in failed : from "+ source_url + " to "+ dest_url
        elif (fs["fs_type"] =="gridftp"):
            try:
                cmd = "globus-url-copy  -cd  %s %s"%(source_url, dest_url)
                os.system(cmd)
            except saga.exception, e:
                error_msg = "File stage in failed : from "+ source_url + " to "+ dest_url

        elif (fs["fs_type"] == "scp"):
             try:
                 cmd = "scp -r %s %s"%(source_url, dest_url)
                 self.logger.info(cmd)
                 os.system(cmd)
             except saga.exception, e:
                 error_msg = "File stage in failed : from "+ source_url + " to "+ dest_url
        return None


    def submit_wu(self,wu):
        jd = saga.job.description()
        jd.executable = wu["executable"]
        jd.number_of_processes = wu["number_of_processes"]
        jd.spmd_variation = wu["spmd_variation"]
        jd.arguments = [wu["arguments"],]
        jd.environment = wu["environment"].split(",")
        jd.working_directory = wu["working_directory"]
        jd.output =  wu["output"]
        jd.error = wu["error"]
        subjob = self.mjs[int(wu["resource"])].create_job(jd)
        subjob.run()
        print "Submited sub-job "+ "."
        self.jobs.append(subjob)
        self.job_start_times[subjob]=time.time()
        self.job_states[subjob] = subjob.get_state()
        self.logger.info( "jd.number_of_processes " + str(jd.number_of_processes))
        self.logger.info( "jd exec " + jd.executable)



    #get the number of wus and wait till they finish
    def wait_for_wus(self,number_of_jobs):

            print "************************ All Jobs submitted ************************" +  str(number_of_jobs)
            while 1:
                finish_counter=0
                result_map = {}
                for i in range(0, number_of_jobs):
                    old_state = self.job_states[self.jobs[i]]
                    state = self.jobs[i].get_state()
                    if result_map.has_key(state) == False:
                        result_map[state]=0
                    result_map[state] = result_map[state]+1
                    #print "counter: " + str(i) + " job: " + str(jobs[i]) + " state: " + state
                    if old_state != state:
                        print "Job " + str(self.jobs[i]) + " changed from: " + old_state + " to " + state
                    if old_state != state and self.has_finished(state)==True:
                         print "Job: " + str(self.jobs[i]) + " Runtime: " + str(time.time()-self.job_start_times[self.jobs[i]]) + " s."
                    if self.has_finished(state)==True:
                         finish_counter = finish_counter + 1
                    self.job_states[self.jobs[i]]=state

                print "Current states: " + str(result_map)
                time.sleep(5)
                self.logger.info("Current states: " + str(result_map))
                if finish_counter == number_of_jobs:
                    break


