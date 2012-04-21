# Copyright Sharath Maddineni(2010-2011) smaddieni@cct.lsu.edu
import os
import time
import ConfigParser
import sys


from subprocess import Popen, call, PIPE

#DARE home dir
DAREHTHP_HOME = os.path.abspath(os.path.join(os.path.abspath(__file__),"..", "..", ".."))
sys.path.insert(0,DAREHTHP_HOME)

import darehthp.lib.modelconnector as jobmodel_helper

DARE_HOME = DAREHTHP_HOME + "/darehthp/lib/DARE/"


class JobMonitor(object):
    def __init__(self):
        pass
    def start_job_monitor(self):
       try:
           while True:
               newjobids = jobmodel_helper.check_new_jobs()
               if (newjobids[0] != "nojobs"):
                   print "new jobs\n \n \n"
                   for jobid in newjobids:
                       self.start_job(jobid)
               time.sleep(10)

       except Exception, e:
            print 'Unable to process in worker thread: ' + str(e)

    def start_job(self, jobid):
        print "running job with id %s"%jobid
        jobid = str(jobid)
        working_directory = os.path.join(DARE_HOME, "darefiles/", str(jobid))
        conffile = os.path.join(working_directory , str(jobid) + "-job.cfg")
        os.system("mkdir -p "+ working_directory)
        self.prepare_conf(jobid, conffile)
        jobmodel_helper.update_job_status(jobid, 2)
        # start the dare here:

        job_type = jobmodel_helper.get_jobtype(jobid)
        if(job_type == "tophatfusion"):
            exec_file = "tophatfusion_dare.py"
        elif(job_type == "chipseq"):
             mapping_tool = jobmodel_helper.get_mapping_tool(jobid)
             print "mapping toool \n\n\n", mapping_tool
             if (mapping_tool == "BOWTIE"):
                 exec_file = "scalable_chipseq_2_dare.py"
             else:
                 exec_file = "scalable_chipseq_dare.py"
        else:
            exec_file = "bfast_dare.py"

        p1 = Popen(["python", os.path.join(DARE_HOME,"examples",exec_file), "-c", conffile], stdout=PIPE)
        print "p1.pid",p1.pid
        jobmodel_helper.update_job_pid(jobid, p1.pid)

        #sts = os.waitpid(p1.pid, 0)[1]

        #update_job_status(jobid, 4)

        print '\n completed starting job%s' %jobid


    def prepare_conf(self, jobid, conffile):
        config = ConfigParser.ConfigParser()
        cfgfile = open(conffile,'w')
        newjobinfo = jobmodel_helper.get_jobinfo(jobid)

        section_name = 'JOB'
        config.add_section(section_name)
        config.set(section_name ,"jobid" , jobid)

        config.set(section_name ,"dare_home", DARE_HOME)
        for jobinfo in newjobinfo:
            config.set(section_name ,jobinfo.key , jobinfo.value)

        config.write(cfgfile)
        cfgfile.close()



if __name__ == '__main__':
   monitor =JobMonitor()
   monitor.start_job_monitor()
   #print jobmodel_helper.get_job_pid(5)
