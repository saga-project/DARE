#!/usr/bin/env python
import sys
import getopt
import saga
import time
import pdb
import os
import traceback
import bigjob
import logging
import many_job
import ConfigParser
import optparse
import uuid

def initialize(conf_filename):
    adams_config = ConfigParser.ConfigParser()
    adams_config.read(conf_filename)
    sections = adams_config.sections()
    return adams_config


def has_finished(state):
        state = state.lower()
        if state=="done" or state=="failed" or state=="canceled":
            return True
        else:
            return False

def sub_jobs_submit(job_type, subjobs_per_resource, number_of_jobs,jd_executable, jd_number_of_processes ):
  
        jobs = []
        job_start_times = {}
        job_states = {}
        jd = saga.job.description()
        affinity = 0

        for i in range(0, int(number_of_jobs)):
   
            if len(machines_used) > 1:
                if (i+1) > (int(subjobs_per_resource)):
                    affinity= 1 
            
            if  jd_executable == "bfast":
                 jd_executable_use = bioscope_exe[affinity] + "/bfast"
            else:
                 jd_executable_use = jd_executable
         
            # create job description
            jd = saga.job.description()
            print jd_executable_use
            jd.executable = jd_executable_use
            jd.number_of_processes = jd_number_of_processes
            jd.spmd_variation = "single"


            if job_type == "reads":
                jd.arguments = ["-n",  "%s" %(bfast_reads_num[affinity]),  
                                "-o", "%s/reads.%s" %(bfast_reads_dir[affinity], bfast_uuid),
                                 "%s/*.csfasta"%(bfast_raw_reads_dir),
                                 "%s/*.qual" %(bfast_raw_reads_dir)]
                                  
            elif job_type == "count":
                jd.arguments = [" -altr" ,"%s/reads*" %(bfast_reads_dir[affinity]),  
                                "|",  "/usr/bin/wc", "-l" , 
                                ">", "%s/out.%s.txt"%(bfast_raw_reads_dir[affinity], bfast_uuid)]
                                
            elif job_type == "matches":
                jd.arguments = ["match",  
                                "-f",  "%s/%s.fa" %( bfast_ref_genome_dir[affinity], refgnome) , 
                                "-A",  "1",
                                "-r",  "%s/reads.%s.fastq"%(bfast_reads_dir[affinity], i+1),
                                #"-r",  "%s/reads.%s.%s.fastq"%(bfast_reads_dir[affinity], bfast_uuid, i+1),
                                "-n" ,"8" ,
                                "-T" , "%s" %(bfast_tmp_dir[affinity]),
                                ">" , "%s/bfast.matches.file.%s.%s.bmf" %(bfast_matches_dir[affinity],refgnome,i+1)] 
                                
            elif job_type == "localalign":
                jd.arguments = ["localalign", 
                                "-f",  "%s/%s.fa"%(bfast_ref_genome_dir[affinity], refgnome),
                                "-A", "1",
                                "-m", "%s/bfast.matches.file.%s.%s.bmf"%(bfast_matches_dir,refgnome,i+1),
                                ">", "%s/bfast.aligned.file.%s.%s.baf" %(bfast_localalign_dir,refgnome,i+1)]
                                
            elif job_type == "postprocess":
                jd.arguments = ["postprocess"
                                "-f",  "%s/%s.fa" %(bfast_ref_genome_dir[affinity], refgnome),
                                "-A",  "1" ,
                                "-i", "%s/bfast.aligned.file.%s.%s.baf" %(bfast_localalign_dir[affinity],refgnome,i+1), 
                                ">", "%s/bfast.reported.file.%s.%s.sam" %(bfast_reported_dir[affinity],refgnome,i+1)]     
            else:
                jd.arguments = [""]
            
            jd.environment = ["affinity=affinity%s"%(affinity)]
            print "affinity%s"%(affinity)
            jd.working_directory = work_dir[affinity]
            jd.output =  os.path.join(work_dir[affinity], "stdout_" + job_type + "-"+ str(bfast_uuid)+"-"+ str(i) + ".txt")
            jd.error = os.path.join(work_dir[affinity], "stderr_"+ job_type + "-"+str(bfast_uuid)+ "-"+str(i) + ".txt")
            subjob = mjs.create_job(jd)
            subjob.run()
            print "Submited sub-job " + "%d"%i + "."
         
            jobs.append(subjob)
            job_start_times[subjob]=time.time()
            job_states[subjob] = subjob.get_state()
            logger.info( job_type + "subjob " + str(i))
            logger.info( "jd.number_of_processes " + str(jd.number_of_processes))
            for item in jd.arguments:
                logger.info( "jd.arguments" + item)
            logger.info("affinity%s"%(affinity))
            logger.info( "jd exec " + jd.executable)
            
        #number_of_jobs = int(end_of_subjobs) - int(start_of_subjobs)
        
        print "************************ All Jobs submitted ************************" +  str(number_of_jobs)
        while 1:
            finish_counter=0
            result_map = {}
            for i in range(0, int(number_of_jobs)):
                old_state = job_states[jobs[i]]
                state = jobs[i].get_state()
                if result_map.has_key(state) == False:
                    result_map[state]=0
                result_map[state] = result_map[state]+1
                #print "counter: " + str(i) + " job: " + str(jobs[i]) + " state: " + state
                if old_state != state:
                    print "Job " + str(jobs[i]) + " changed from: " + old_state + " to " + state
                if old_state != state and has_finished(state)==True:
                     print "Job: " + str(jobs[i]) + " Runtime: " + str(time.time()-job_start_times[jobs[i]]) + " s."
                if has_finished(state)==True:
                     finish_counter = finish_counter + 1
                job_states[jobs[i]]=state

            print "Current states: " + str(result_map)
            time.sleep(5)
            logger.info("Current states: " + str(result_map))
            if finish_counter == int(number_of_jobs):
                break

                  


""" Test Job Submission via ManyJob abstraction """
if __name__ == "__main__":
    config = {}

    #cwd = "/home/cctsg/pylons/DARE-BIOSCOPE/darebioscope/lib/adams/"
    cwd = os.getcwd()

    bfast_uuid = uuid.uuid1()
    
   # bfast_uuid = "6ff33a54-5a27-11e0-b26f-d8d385abb2b0"
    # parse conf files
    parser = optparse.OptionParser()
    
    parser.add_option("-j", "--job-conf", dest="job_conf", help="job configuration file")

    (options, args) = parser.parse_args()
    machines_used = []
    #parse job conf file
    job_conf = options.job_conf
    config = initialize(job_conf)
    refgnome = config.get('Bfast', 'refgnome')
    job_id = config.get('Bfast', 'job_id')
    confss = config.get('Bfast', 'machine_use')
    #print confss.replace(' ','').split(',')
    machines_used = confss.replace(' ','').split(',')
    #print machines_used
    dir_calc=config.get('Bfast', 'workdir')

    work_dir = []
    bioscope_exe = []  
    gram_url= []
    re_agent= []
    allocation= []
    queue = []
    bfast_raw_reads_dir = [] 
    bfast_reads_num = [] 
    bfast_reads_dir = []
    bfast_ref_genome_dir = [] 
    bfast_tmp_dir = []
    bfast_matches_dir = []
    bfast_num_cores = []
    bfast_localalign_dir = []
    bfast_reported_dir = []
    jd_executable_bfast = []
    jd_executable_solid2fastq = []
    cores_per_node = []
    machine_proxy = []
    
    #parse adams conf file
    adams_conf = os.path.join(cwd, "resource.conf")
    config = initialize(adams_conf)
    
    for machine in machines_used:
        print machine
        work_dir.append(config.get(machine, 'work_dir'))
        #print "wor_dir"+work_dir
        machine_proxy.append(config.get(machine, 'machine_proxy'))
        bioscope_exe.append(config.get(machine, 'bioscope_exe'))
        gram_url.append(config.get(machine, 'gram_url')) 
        re_agent.append(config.get(machine, 're_agent'))
        allocation.append(config.get(machine, 'allocation'))
        queue.append( config.get(machine, 'queue'))
        bfast_raw_reads_dir.append(config.get(machine, 'bfast_raw_reads_dir'))
        bfast_reads_num.append(config.get(machine, 'bfast_reads_num') )
        bfast_reads_dir.append(config.get(machine, 'bfast_reads_dir') )
        bfast_ref_genome_dir.append(config.get(machine, 'bfast_ref_genome_dir') )
        bfast_tmp_dir.append(config.get(machine, 'bfast_tmp_dir') )
        bfast_matches_dir.append(config.get(machine, 'bfast_matches_dir'))
        bfast_num_cores.append(config.getint(machine, 'bfast_num_cores_threads'))
        bfast_localalign_dir.append(config.get(machine, 'bfast_localalign_dir'))
        bfast_reported_dir.append(config.get(machine, 'bfast_reported_dir'))
        cores_per_node.append(config.get(machine, 'cores_per_node'))
    
    
   #parse dare conf file
    dare_conf = os.path.join(cwd, "dare.conf")
    config = initialize(dare_conf)
    refgnome = config.get('hg18-ch21', 'filename')
    
    LOG_FILENAME = os.path.join(cwd, 'logfiles', '%s_%s_log_bfast.txt'%(job_id, bfast_uuid))

    logger = logging.getLogger('adams_bfast_manyjob')
    hdlr = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)


    logger.info("Job id  is "  + str(job_id) )
    #logger.info("Working Dir is " + work_dir )  
    logger.info("Machine used is " + machines_used[0] )
    #logger.info("Reference GNOME " + refgnome)
    #logger.info("number_of_jobs " + str(number_of_jobs)) 
    
    
    try:
        #print "ManyJob load test with " + str(number_of_jobs) + " jobs."
        starttime=time.time()
        
        #print bioscope_exe[0]
        
        # submit via mj abstraction
        resource_list = []

        i=0
        mjs = []
        for i in range(0,len(machines_used) ):
            print machine_proxy[i]
            resource_list.append({"gram_url" : gram_url[i], "walltime": "80" ,
                                   "number_cores" : str(int(16)*2),
                                   "cores_per_node":cores_per_node[i],"allocation" : allocation[i],
                                   "queue" : queue[i], "re_agent": re_agent[i], "userproxy":machine_proxy[i], "working_directory": work_dir[i], "affinity" : "affinity%s"%(i)})
            logger.info("gram_url" + gram_url[i])
            logger.info("affinity%s"%(i))
        print "Create manyjob service " 
        mjs = many_job.many_job_service(resource_list, "advert.cct.lsu.edu")
            
            
        """ 
        prep_reads_starttime = time.time()

        ### run the preparing read files step
        
        sub_jobs_submit("new", "4" ,"8","/bin/date", "2") ##dummy job for testing

        #sub_jobs_submit("reads" , "1", jd_executable_solid2fastq, str(bfast_num_cores))
        
        prep_reads_runtime = time.time()-prep_reads_starttime
        logger.info("prepare reads Runtime: " + str( prep_reads_runtime))

        
        # job to get the count of read files
        sub_jobs_submit("count",  "1", "/bin/ls", "8")
       
       
        # transfer the files
        output = saga.filesystem.file("gridftp://qb1.loni.org//%s/out.%s.txt"%(bfast_raw_reads_dir, bfast_uuid))
        output.copy("file://localhost//%s/logfiles/"%(cwd))
        
        
        f = open(r'%s/logfiles/out.%s.txt'%(cwd, bfast_uuid))
        num_reads=f.readline()
        f.close()
        """    
    
        matches_starttime = time.time()
        
        ### run the matching step
        #sub_jobs_submit("new", "16","32", "/bin/date", "2") ##dummy job for testing
        sub_jobs_submit("matches" , "16", "32", "bfast", "2")
        
        matches_runtime = time.time()-matches_starttime
        logger.info("Matches Runtime: " + str( matches_runtime) )
        """ 
        ### run the local-alignment step
        localalign_starttime = time.time()
        
        #sub_jobs_submit("new", "4", "/bin/date", "2") ##dummy job for testing
        sub_jobs_submit("localalign" , num_reads, jd_executable_bfast, str(bfast_num_cores))

        localalign_runtime = time.time() - localalign_starttime
        logger.info("localalign Runtime: " + str( localalign_runtime) )

        postprocess_starttime = time.time()

        ### run the postprocess step        
        #sub_jobs_submit("new", "4", "/bin/date", "2") ##dummy job for testing
        sub_jobs_submit("postprocess" ,num_reads , jd_executable_bfast, str(bfast_num_cores))

        postprocess_runtime = time.time() - postprocess_starttime
        logger.info("Postporcess Runtime: " + str( postprocess_runtime) )
        """
        mjs.cancel()
        
    except:
        traceback.print_exc(file=sys.stdout)
        try:
            mjs.cancel()
            
        except:
            pass
