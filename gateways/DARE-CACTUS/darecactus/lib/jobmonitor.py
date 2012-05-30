# Copyright Sharath Maddineni(2010-2011) smaddieni@cct.lsu.edu
import os
import time
import ConfigParser
import sys
import random
import string
from subprocess import Popen, call, PIPE

from threading import Thread

#DARE home dir
DARECACTUS_HOME = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))
sys.path.insert(0, DARECACTUS_HOME)

from darecactus.lib.ormconnector import check_new_jobs, get_jobinfo, get_job_file, update_job_status, get_jobtype, update_job_pid, RUNNING, NEW
DARE_CACTUS_JOB_DIR = os.path.join(os.getenv('HOME'), "DAREJOBS/darecactus")


class JobMonitor(object):
    def __init__(self):
        pass

    def start_job_monitor(self):
        while True:
            newjobids = check_new_jobs()
            if (newjobids[0] != "nojobs"):
                print "New Job:"
                for jobid in newjobids:
                    #job status
                    print "\n Starting Job with id %s" % jobid
                    js = JobStarter(jobid)
                    js.start()
            #import pdb; pdb.set_trace()

            time.sleep(10)


class JobStarter(Thread):

    def __init__(self, jobid):
        Thread.__init__(self)
        self.jobid = str(jobid)
        self.working_directory = os.path.join(DARE_CACTUS_JOB_DIR, self.jobid)
        os.system("mkdir -p  " + self.working_directory)

        self.prepare_files()
        self.prepare_conf()

    def run(self):

        job_type = get_jobtype(self.jobid)

        exec_file = "cactus_build_dare.py"
        cmd = os.path.join(DARECACTUS_HOME, 'darecactus', 'lib', 'DARE', "examples", exec_file)
        print cmd, " -c ", self.conffile
        p1 = Popen(['python', cmd,  " -c ", self.conffile], stdout=PIPE)

        update_job_pid(self.jobid, p1.pid)
        update_job_status(self.jobid, RUNNING)
        print "p1.pid", p1.pid
        p1.wait()

        update_job_status(self.jobid, RUNNING)
        exec_file = "cactus_dare.py"
        p2 = Popen(['python', os.path.join(DARECACTUS_HOME, 'darecactus', 'lib', 'DARE', "examples", exec_file), "-c", self.conffile], stdout=PIPE)
        print "p2.pid", p2.pid
        update_job_pid(self.jobid, p2.pid)
        p2.wait()
        #update_job_status(jobid, 4)
        print 'Job %s  Started  ' % self.jobid

    def prepare_conf(self):

        self.conffile = os.path.join(self.working_directory, str(self.jobid) + "-job.cfg")
        config = ConfigParser.ConfigParser()
        newjobinfo = get_jobinfo(self.jobid)

        section_name = 'JOB'
        config.add_section(section_name)
        config.set(section_name, "jobid", self.jobid)

        config.set(section_name, "local_darejob_dir", os.path.join(DARE_CACTUS_JOB_DIR, self.jobid))

        for jobinfo in newjobinfo:
            config.set(section_name, jobinfo.key, jobinfo.value)

        config.set(section_name, "thornfile", self.thorname_full)
        config.set(section_name, "parfile", self.parname_full)

        config.set(section_name, "paramname", self.parname)

        config.set(section_name, 'cactus_build_name', "%s_build" % self.thornname.split('.')[0])
        cactus_sim_name = "%s_sim_%s" % (self.parname.split('.')[0], ''.join(random.choice(string.ascii_letters) for x in range(4)))
        config.set(section_name, 'cactus_sim_name', cactus_sim_name)

        cfgfile = open(self.conffile, 'w')
        config.write(cfgfile)
        cfgfile.close()

    def prepare_files(self):

        self.thornname, thornfile = get_job_file(self.jobid, "thorn")
        self.parname, parfile = get_job_file(self.jobid, "par")

        self.thorname_full = os.path.join(self.working_directory, self.thornname)
        self.parname_full = os.path.join(self.working_directory, self.parname)

        thornfile_c = open(self.thorname_full, 'w')
        parfile_c = open(self.parname_full, 'w')

        thornfile_c.write(thornfile)
        parfile_c.write(parfile)

if __name__ == '__main__':

    monitor = JobMonitor()
    monitor.start_job_monitor()
    #print jobmodel_helper.get_job_pid(5)
