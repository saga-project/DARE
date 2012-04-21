import os
import sys
import time
import ConfigParser
import uuid

import optparse


"""

major change log 
moving dict_section to dare.py
change the dict_section(job_config, "JOB") to section name 2nd argument
steps staring point (0 or 1?)
config to dare_config

change the directory structre
---examples/example_dare.py

"""

"""
###### how this works
1. read conf file from the web   
2. define the resource list
3. define the task/data movement list
4. Write the DARE config file
5. Start DARE using the above config file
"""


if __name__ == '__main__':
    dare_uuid = uuid.uuid1()

###################################################################################################
##########          read conf file got from the web                     ###########################
###################################################################################################
 
    # parse conf files
    parser = optparse.OptionParser()    
    parser.add_option("-c", "--conf_job", dest="conf_job", help="job configuration file")
    (options, args) = parser.parse_args()


    job_config = ConfigParser.ConfigParser()
    confjob = options.conf_job
    job_config.read(confjob)
    
    DARE_HOME = job_config.get('JOB', "dare_dir")       
    os.environ["DARE_HOME"]=DARE_HOME
    sys.path.insert(0, DARE_HOME)
    
    from dare import dict_section, dare
    
    try:
        from dare import dict_section, dare
    except:
        print "failed to import dare"
        sys.exit()
    
    
    
    job_conf = dict_section( job_config, "JOB")

    
    #print job_conf
    #get the resources used from job configuration file   
    resources_used = [job_conf["machine"]]
    jobid = job_conf["jobid"] 
    #get the dare_cwd
    
    #TODO calculate number of nodes an walltime here now its static
    number_nodes = [1] 
    walltime  = [100]    
    
    #application working directory
    working_directory = os.path.join(DARE_HOME, "darefiles/", str(jobid)) 
    
    #start building the dare conf file for dare
    dare_config = ConfigParser.ConfigParser()

###################################################################################################
##########          define resource list                        ###################################
###################################################################################################

    #read the resource conf file
    resource_conf_file = os.path.join(DARE_HOME, 'examples/example/resource.cfg')
    resource_config = ConfigParser.ConfigParser()
    resource_config.read(resource_conf_file)  
    
    for i in range (0,len(resources_used)):   
        resource_conf = dict_section( resource_config, resources_used[i])
        section_name = "resource_" + str(i)
        dare_config.add_section(section_name)        
        #constant parameters
        dare_config.set(section_name, "resource_url", resource_conf["resource_url"] )
        dare_config.set(section_name, "processes_per_node",  resource_conf["cores_per_node"])
        dare_config.set(section_name, "allocation", resource_conf["allocation"]) 
        dare_config.set(section_name, "queue", resource_conf["queue"]) 
        dare_config.set(section_name, "bigjob_agent", resource_conf["bigjob_agent"])
        dare_config.set(section_name, "userproxy", resource_conf["userproxy"])
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "filetransfer_url", resource_conf["filetransfer_url"])
        
        #changing parameters from job to job
        dare_config.set(section_name, "walltime", walltime[i])
        dare_config.set(section_name, "number_nodes",  number_nodes[i])
  
        #todo add resource list in the middle

  
    #application specific important for building a workflow
    #add tasks here
    num_step_wus = {} 
    step_type = {}
    wus_count = 0 
    
###################################################################################################
##########          step =0(compute)         ######################################################
###################################################################################################

    #following line mandotory for each step
    step = 0
    num_step_wus[step]= 1
    step_type[step] = "compute"
    
    #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/example/example_1_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section(step_config, "common")
    step_resource_conf = dict_section( step_config, resources_used[0])
    
    # Using a loop here but this can/will be static
    for i in range (0, num_step_wus[step]):   
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf["arguments"])
        dare_config.set(section_name, "environment",step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        ######
        ######increase wu count
        ######
        wus_count = wus_count + 1

###################################################################################################
###########             step = 1 (data)      ######################################################
###################################################################################################    
    
    step = 1
    num_step_wus[step]= 1
    step_type[step] = "data"
    
    # Using a loop here but this can/will be static
    for i in range (0, num_step_wus[step]):   
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
        dare_config.set(section_name, "appname", "file_transfer")
        dare_config.set(section_name, "fs_type", "scp")
        dare_config.set(section_name, "source_url", "/home/cctsg/backup/test.txt")
        dare_config.set(section_name, "dest_url", "cctsg@cyder.cct.lsu.edu:/home/cctsg/backup/tt-"\
        + str(i)+ ".txt") 
        
        ######increase wu count
        wus_count = wus_count + 1

####################################################################################################
##########          step =2 (compute)         ######################################################
####################################################################################################
     
    step = 2
    num_step_wus[step]= 1
    step_type[step] = "compute"
        
    step_conf_file = os.path.join(DARE_HOME, 'examples/example/example_2_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    
    # Using a loop here but this can/will be static
    for i in range (0, num_step_wus[step]):   
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf["arguments"])
        dare_config.set(section_name, "environment",step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        ######increase wu count
        wus_count = wus_count + 1  


    # we have the number of tasks per each step and resource list at this point


###################################################################################################
##########    finally      define DAREJOB  for dare.py   ##########################################
###################################################################################################    
    
    section_name = 'DAREJOB'
    dare_config.add_section(section_name)
    dare_config.set(section_name, "jobid", jobid) 
    dare_config.set(section_name, "updatedb", "true")
    dare_config.set(section_name, "dare_home", DARE_HOME)
    dare_config.set(section_name, "num_resources", len(resources_used)) 
    dare_config.set(section_name, "num_steps", len(num_step_wus)) 
    dare_config.set(section_name, "log_filename", os.path.join(working_directory, str(jobid) +"-dummy-darelog.txt"))
    
    #change it to dare_config.append()
    wus_count_2 = 0
    for i in range (0, len(num_step_wus)):    
        step_wus_string = "" 
        for x in range (0, num_step_wus[i]): 
            step_wus_string = step_wus_string + "wu_" + str( wus_count_2)
            if (x != (num_step_wus[i] -1)):
                step_wus_string = step_wus_string + ", "
            wus_count_2 =  wus_count_2 + 1
        ## add for each section wu's    
        dare_config.set(section_name , "step_" + str(i), step_wus_string)
        
    ## making  ft_string to communicate it to dare
    
    ft_step_string = ""
    for i in range (0, len(num_step_wus)): 
        if (step_type[i] == "data"):
            ft_step_string = ft_step_string + "step_" + str(i)
            if (x != (num_step_wus[i] -1)):
                ft_step_string = ft_step_string + ", "
            
    dare_config.set(section_name , "ft_steps", ft_step_string) 
    

    
###############  write the config file for dare.py        #########################################
    try:
        dare_conffile =  os.path.join(working_directory, str(jobid) +"-darejob.cfg") 
        dare_cfgfile = open(dare_conffile,'w')
        dare_config.write(dare_cfgfile)
        dare_cfgfile.close() 
    except:
        print "Could not write DARE config file"
        sys.exit(0);

    #start dare
    #print dare_conffile
    
    #try:
    dare_instance = dare(dare_conffile)
    dare_instance.run()
    #except  :
     #   print "could not a start dare instance"
