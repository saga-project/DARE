#!/usr/bin/env python
""" Example application demonstrating job submission via bigjob 
    diane implementation of BigJob is used
"""


import sys
import saga
import getopt
import time
import pdb
import os
import traceback
import logging
import ConfigParser
import optparse
import uuid

# BigJob implementation can be swapped here by importing another implementation,
# e.g. condor, cloud, azure, diane

cwd = os.getcwd()
BIGJOB_HOME= "/home/cctsg/examples/bigjob/branches/bigjob_overhaul/"
sys.path.append(BIGJOB_HOME)

import troy


global  uows #, job_start_times, job_states
uows = []
#job_start_times = {}
#job_states = {}

#initialize the conf files
def initialize(conf_filename):
    dare_config = ConfigParser.ConfigParser()
    dare_config.read(conf_filename)
    sections = dare_config.sections()
    return dare_config

def has_finished(state):
        state = state.lower()
        if state=="done" or state=="failed" or state=="canceled":
            return True
        else:
            return False
            
# file stager for grids and clouds
#TODO: should be SAGA based and pilot store
def file_stage(source_url, dest_url):

    print "(DEBUG) Now I am tranferring the files from %s to %s"%(source_url, dest_url)
    #fgeuca for clouds
    if dest_url.startswith("fgeuca"):
        try:
            #for cloud files
            cmd = "scp  -r -i /path/to/smaddi2.private %s %s"%(source_url, dest_url)
            os.system(cmd)
        except saga.exception, e:
            error_msg = "File stage in failed : from "+ source_url + " to "+ dest_url
    else:
        try:
            cmd = "globus-url-copy  -cd  %s %s"%(source_url, dest_url)
            os.system(cmd)
        except saga.exception, e:
            error_msg = "File stage in failed : from "+ source_url + " to "+ dest_url
    return None

# method to submit tasks to based of affinity
#jd_executable-which executable should be used
#job_type - of job reads step, matching step etc, to determine the parameters
#affinity -- the tasks affinity to make sure which one it should bind
#subjobs_start # the task number which will different for multiple resources/affinities
#number_of_jobs # number of tasks for particular affinity
#jd_number_of_processes #processes per task

def sub_jobs_submit( jd_executable, job_type, affinity ,  subjobs_start,  number_of_jobs, jd_number_of_processes):
                                 
        jd = saga.job.description()
        
        for i in range(subjobs_start, int(number_of_jobs) + int(subjobs_start) ):

            #pick the executble different for preparing read files
            if  jd_executable == "bfast":
                 jd_executable_use = bfast_exe[affinity] + "/bfast"
            elif jd_executable == "solid2fastq":   
                 jd_executable_use = bfast_exe[affinity] + "/solid2fastq"
 
            else:
                 jd_executable_use = jd_executable
            
            # create job description
            uowd = troy.uow_description()

            print jd_executable_use
            uowd.set_attribute('Executable', jd_executable_use)
            uowd.set_attribute('NumberOfProcesses', str(jd_number_of_processes))

            uowd.set_attribute('SPMDVariation', 'single')
            
            # choose the job arguments based on type of job
            if job_type == "reads":
                uowd.set_vector_attribute('Arguments', \
                        ["-n",  "%s" %(bfast_reads_num[affinity]),  
                        "-o", "%s/%s.%s" %(bfast_reads_dir[affinity],shortreads_name ,dare_uuid),
                        "%s/*.csfasta"%(bfast_raw_reads_dir[affinity]),
                        "%s/*.qual" %(bfast_raw_reads_dir[affinity])])
                                  
            elif job_type == "count":
                uowd.set_vector_attribute('Arguments', \
                                [" -altr" , "%s/%s.%s.*" %(bfast_reads_dir[affinity],shortreads_name ,dare_uuid), 
                                "|",  "/usr/bin/wc", "-l" , 
                                ">", "%s/out.%s.txt"%(bfast_raw_reads_dir[affinity], dare_uuid)])
                                
            elif job_type == "matches":
                uowd.set_vector_attribute('Arguments', \
                         ["match",  
                         "-f",  "%s/%s.fa" %( bfast_ref_genome_dir[affinity], refgenome) , 
                         "-A", encoding_space, 
                         "-r",  "%s/%s.%s.fastq"%(bfast_reads_dir[affinity], shortreads_name,i+1),
                         "-n" ,str(jd_number_of_processes) ,
                         "-T" , "%s" %(bfast_tmp_dir[affinity]),
                         ">" , "%s/bfast.matches.file.%s.%s.%s.bmf" %(bfast_matches_dir[affinity],dare_uuid,refgenome,i+1)])  

            elif job_type == "localalign":
                uowd.set_vector_attribute('Arguments', \
                                ["localalign", 
                                "-f",  "%s/%s.fa"%(bfast_ref_genome_dir[affinity], refgenome),
                                "-A", encoding_space,
                                "-m", "%s/bfast.matches.file.%s.%s.%s.bmf"%(bfast_matches_dir[affinity],dare_uuid,refgenome,i+1),
                                ">", "%s/bfast.aligned.file.%s.%s.%s.baf" %(bfast_localalign_dir[affinity],dare_uuid,refgenome,i+1)])
                                
            elif job_type == "postprocess":
                uowd.set_vector_attribute('Arguments', \
                                ["postprocess",
                                "-f",  "%s/%s.fa" %(bfast_ref_genome_dir[affinity], refgenome),
                                "-A",  encoding_space,
                                "-i", "%s/bfast.aligned.file.%s.%s.%s.baf" %(bfast_localalign_dir[affinity],dare_uuid,refgenome,i+1),
                                ">", "%s/bfast.postprocess.file.%s.%s.%s.sam" %(bfast_postprocess_dir[affinity],dare_uuid,refgenome,i+1)])     
            
            elif job_type == "hostname":
                uowd.set_vector_attribute('Arguments', \
                               ['-f', '>', 'hostname%s.txt'%i, ';', '/bin/sleep', '15'])
                 
            
            else:
                uowd.set_vector_attribute('Arguments', [""])
            
            #jd.environment = ["affinity=affinity%s"%(affinity)]
            print "affinity%s"%(affinity)
            uowd.set_attribute('WorkingDirectory', work_dir[affinity])
            uowd.set_attribute('Output', os.path.join(work_dir[affinity], "stdout_" + job_type + \
                              "-"+ str(dare_uuid)+"-"+ str(i) + ".txt"))
            uowd.set_attribute('Error', os.path.join(work_dir[affinity], "stderr_"+ job_type + \
                              "-"+str(dare_uuid)+ "-"+str(i) + ".txt"))

            uows.append(bj.assign_uow(uowd))
            
            print "Submited sub-job " + "%d"%i + "."
                     
          
            logger.info( job_type + "subjob " + str(i))
            logger.info( "jd.number_of_processes " + str(jd_number_of_processes))
            print "jd.arguments"
           
            logger.info("affinity%s"%(affinity))
            logger.info( "jd exec " + jd_executable_use)
            
 
#get the number of tasks and wait till they finish 
def wait_for_jobs(number_of_jobs):               

        print "************************ All Jobs submitted ************************" +  str(number_of_jobs)
        while 1:
            uow_states = set()
            for i in range(len(uows)):
                uow_states.add(uows[i].get_state())
            print 'UoW state:', uow_states
            if set([saga.job.job_state.New,saga.job.job_state.Unknown, \
                saga.job.job_state.Running]).isdisjoint(uow_states):
                break
            try:
                time.sleep(5)
            except:
                break


if __name__ == "__main__":
    config = {}
    print "DARE started at ", time.time()
    #get the current working directory
    cwd = os.getcwd()

    dare_uuid = uuid.uuid1()
    
    # parse conf files
    parser = optparse.OptionParser()    
    parser.add_option("-j", "--job-conf", dest="job_conf", help="job configuration file")
    (options, args) = parser.parse_args()
    
    resources_used = []
    global shortreads_name

    
    # Start BigJob
    bj = troy.Bigjob()

    #parse job conf file
    job_conf = options.job_conf
    config = initialize(job_conf)
    
    print job_conf
    
    refgenome = config.get('Bfast', 'refgenome')
    job_id = config.get('Bfast', 'job_id')
    machu = config.get('Bfast', 'resources_use')
    resources_used = machu.replace(' ','').split(',')    
    # resources_job_count is the corresponding number of tasks per 
    # resouce for the resources that are mentioned.
    # e.g. the number of input files to process per resource, or the 
    # number of simulations to run
    machs = config.get('Bfast', 'resources_job_count')
    resources_job_count = machs.replace(' ','').split(',')
    #type of reference genome
    refgenome = config.get('Bfast', 'refgenome')
    #location of reference genome
    source_refgenome =config.get('Bfast', 'source_refgenome')
    source_raw_reads =config.get('Bfast', 'source_raw_reads')
    source_shortreads =config.get('Bfast', 'source_shortreads')
    ##to check whether to run the prepare_read files step?
    prepare_shortreads = config.get('Bfast', 'prepare_shortreads')
    resource_list = config.get('Bfast', 'resource_list')
    resource_app_list = config.get('Bfast', 'resource_app_list')
    shortreads_name = config.get('Bfast', 'shortreads_name')
    walltime = config.get('Bfast', 'walltime')

    
    work_dir = []
    resource_url= []
    bigjob_agent= []
    allocation= []
    queue = []
    cores_per_node = []
    resource_proxy = []
    ft_name= []
    #parse dare_resource conf file
    
    config = initialize(resource_list)
    
    for resource in resources_used:
        print resource
        
        work_dir.append(config.get(resource, 'work_dir'))
        if (config.get(resource, 'resource_proxy') == "NA") :
           resource_proxy.append(None)
        else:
           resource_proxy.append(config.get(resource, 'resource_proxy'))
        resource_url.append(config.get(resource, 'resource_url')) 
        bigjob_agent.append(config.get(resource, 'bigjob_agent'))
        allocation.append(config.get(resource, 'allocation'))
        queue.append( config.get(resource, 'queue'))
        cores_per_node.append(config.get(resource, 'cores_per_node'))
        ft_name.append(config.get(resource, 'ft_name'))
        
    #dare_bfast conf file application specific config file 
    bfast_exe = []
    bfast_raw_reads_dir = [] 
    bfast_reads_num = [] 
    bfast_reads_dir = []
    bfast_ref_genome_dir = [] 
    bfast_tmp_dir = []
    bfast_matches_dir = []
    bfast_num_cores = []
    bfast_localalign_dir = []
    bfast_postprocess_dir = []
    jd_executable_bfast = []
    jd_executable_solid2fastq = []
    
    config = initialize(resource_app_list)
    
    for resource in resources_used:
        #affinity based, might be same for group resource, should add more cases(define affinity variable)
        if resource.startswith("fgeuca"):
           resource = "fgeuca"        
        bfast_exe.append(config.get(resource, 'bfast_exe'))
        encoding_space = config.get(resource , 'encoding_space')
        bfast_raw_reads_dir.append(config.get(resource, 'bfast_raw_reads_dir'))
        bfast_reads_num.append(config.get(resource, 'bfast_reads_num') )
        bfast_reads_dir.append(config.get(resource, 'bfast_reads_dir') )
        bfast_ref_genome_dir.append(config.get(resource, 'bfast_ref_genome_dir') )
        bfast_tmp_dir.append(config.get(resource, 'bfast_tmp_dir') )
        bfast_matches_dir.append(config.get(resource, 'bfast_matches_dir'))
        bfast_num_cores.append(config.getint(resource, 'bfast_num_cores_threads'))
        bfast_localalign_dir.append(config.get(resource, 'bfast_localalign_dir'))
        bfast_postprocess_dir.append(config.get(resource, 'bfast_postprocess_dir'))                
    
    LOG_FILENAME = os.path.join(cwd, 'dare_files/logfiles/', '%s_%s_log_bfast.txt'%(job_id, dare_uuid))

    logger = logging.getLogger('dare_bfast_manyjob')
    hdlr = logging.FileHandler(LOG_FILENAME)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    logger.info("Job id  is "  + str(job_id) )
    logger.info("Machine used is " + resources_used[0] )
    logger.info("Reference GNOME " + refgenome)
       
    try:  
           
        # submit via mj abstraction        
        
        ## start the big job agents
        resource_list = []
        mjs = []
        
        for i in range(0,len(resources_used) ):
            
            resource_list.append([])
            #calculate exact number of cores to request
            ccpn= int(cores_per_node[i]) 
            crjc= int(resources_job_count[i])
            cbnc= int(bfast_num_cores[i])
            k=0
            if (cbnc*crjc%ccpn !=0):
               k =1
            number_nodes = ccpn * (cbnc*crjc/ccpn +k ) 


            
            jd = troy.bj_description()
             
            print "hello"             
            RESOURCE_URL = "gram://oliver1.loni.org/jobmanager-pbs"
            DEPLOYMENT_LOCATION = '/work/smaddi2/bigjob/'
            jd.set_attribute('NumberOfProcesses', '8') # total number of agents
            jd.set_attribute('ProcessesPerHost', '4') # Ignored?
            jd.set_attribute('Queue', 'workq')
            jd.set_vector_attribute('JobProject', ['loni_jhabig12'])
            jd.set_attribute('WorkingDirectory', DEPLOYMENT_LOCATION)
            jd.set_attribute('WallTimeLimit', '30')
            bj.add_resource(troy.bigjob_type.SAGA, RESOURCE_URL, jd)
            print "Pilot Job/BigJob URL: ", bj.list_resources()
            logger.info("resource_url" + resource_url[i])
            print "Create manyjob service "
            
            RESOURCE_URL = "gram://oliver1.loni.org/jobmanager-pbs"
            DEPLOYMENT_LOCATION = 'gsiftp://oliver1.loni.org/work/smaddi2/bigjob/'
            jd.set_attribute('NumberOfProcesses', '2') # total number of nodes/agents
            jd.set_attribute('ProcessesPerHost', '2') # Ignored? number of workers per node
            jd.set_attribute('Queue', 'workq')
            jd.set_vector_attribute('JobProject', ['loni_jhabig12'])
            jd.set_attribute('WorkingDirectory', DEPLOYMENT_LOCATION)
            jd.set_attribute('WallTimeLimit', '30')
            bj.add_resource(troy.bigjob_type.DIANE, RESOURCE_URL, jd)
            print "Pilot Job/BigJob URL: ", bj.list_resources()
            logger.info("resource_url" + resource_url[i])
            logger.info("affinity%s"%(i))            
            print "Create manyjob service "
            
            


        
        """
        #file transfer step, check if prepare_shortreads parameter is set from job-conf file 
        ### transfer the files index files
        if not (source_refgenome == "NONE"):       
            for i in range(0,len(resources_used) ):
                file_stage("file://%s"%(source_refgenome), ft_name[i]+bfast_ref_genome_dir[i])        
        #tarnsfer raw shortread files to first resource mentioned since it is enough to prepare short reads on resource
        if not (source_raw_reads == "NONE"):       
            file_stage("file://" + source_shortreads, ft_name[0]+bfast_reads_dir[0])                    
          
        if (prepare_shortreads == "true"):          
            prep_reads_starttime = time.time
            #run the preparing read files step
            sub_jobs_submit("solid2fastq","reads", 0 , 1 , 1,int(bfast_num_cores[i]))
            wait_for_jobs(1)
            prep_reads_runtime = time.time()-prep_reads_starttime          
            logger.info("prepare reads Runtime: " + str( prep_reads_runtime))
              
            # job to get the count of number of read files should be used to launch resources
            sub_jobs_submit("count","count", 0 , 1 , 1,int(bfast_num_cores[i]))
            wait_for_jobs(1)
            
            # transfer the read file count file, might not work should debug it first
            output = saga.filesystem.file("%s/%s/out.%s.txt"%(ft_name[0],bfast_raw_reads_dir[i]
                                         , dare_uuid))
            output.copy("file://localhost//%s/dare_files/"%(cwd))        
        
            f = open(r'%s/logfiles/out.%s.txt'%(cwd, dare_uuid))
            num_reads=f.readline()
            f.close()
            #assign shortreads directory
            source_shortreads = ft_name[0]+bfast_reads_dir[affinity] 
        
        ### transfer the prepared read files to other resources
        p=1    
        if not (source_shortreads == "NONE"):       
                for i in range(0,len(resources_used) ):
                    for k in range(p,p+int(resources_job_count[i])):
                        file_stage(source_shortreads+"%s.%s.fastq"%(shortreads_name,k)
                                   , ft_name[i]+bfast_reads_dir[i])     
                    p = p + int(resources_job_count[i])
        total_number_of_jobs=0
        ### run the matching step      
        """
        #sample sub_jobs_submit for reference
        #sub_jobs_submit( jd_executable, job_type, affinity = 0,  subjobs_start = 0 
        #                 ,  number_of_jobs = 0, jd_number_of_processes = 0 ):
               
        matches_starttime = time.time()
        total_number_of_jobs =0
        
        #dummy job
        #sub_jobs_submit("/bin/hostname","hostname", i , total_number_of_jobs #subjobs starts here 
           #                , resources_job_count[i],int(bfast_num_cores[i]))
         
        i  = 0
        resources_job_count[i] = 8
        bfast_num_cores[i] = 2
        sub_jobs_submit("bfast","matches", i , total_number_of_jobs #subjobs starts here 
                           , resources_job_count[i],int(bfast_num_cores[i]))
        logger.info( "resource " + str(i))
        logger.info( "total_number_of_jobs " + str(total_number_of_jobs))
        logger.info( "resources_job_count " + str(resources_job_count[i]))
        logger.info( "int(bfast_num_cores" + str(bfast_num_cores[i]))
            
        total_number_of_jobs = total_number_of_jobs + int(resources_job_count[i])     

        wait_for_jobs(1)
        
        matches_runtime = time.time()-matches_starttime
        logger.info("Matches Runtime: " + str( matches_runtime) )               
                
        bj.cancel()

    except:
        traceback.print_exc(file=sys.stdout)
        try:
            bj.cancel()            
        except:
            pass
