import os
import time
import ConfigParser
import uuid
import dare
import optparse

def dict_section(section, config_parser):
        
        lst = config_parser.items(section)
        dct={}
        for i in range(len(lst)):
            dct[lst[i][0]]=lst[i][1]
        #print dct
        return dct


if __name__ == '__main__':
    dare_uuid = uuid.uuid1()
   
    # parse conf files
    parser = optparse.OptionParser()    
    parser.add_option("-c", "--conf_file", dest="conf_file", help="job configuration file")
    (options, args) = parser.parse_args()

    config = ConfigParser.ConfigParser()
    conf_file = options.conf_file
    config.read(conf_file)
    
    #add most important section here
    conffile = "darefiles/jobconf/2-job.cfg" 
    config = ConfigParser.ConfigParser()
    cfgfile = open(conffile,'w')


    #application dependent parameters    
    num_steps  = 2
    walltime  = 10
    number_nodes = 1 
    resources_used = ["localhost"]
    num_resources = len(resources_used)
    
    #add tasks here
    num_step_wus = [2,2]
    wus_count = 0
    
    #get the dare_cwd
    DARE_WD = "/home/cctsg/install/DARE-NGS/darengs/lib/DARE/"       
    
    section_name = 'DAREJOB'
    config.add_section(section_name)
    config.set(section_name , "jobid", 1) 
    config.set(section_name , "num_resources", num_resources) 
    config.set(section_name , "num_steps", num_steps) 
    config.set(section_name , "ft_steps", "") 
    config.set(section_name , "log_filename", DARE_WD + "darefiles/logfiles/logfile.txt")

    for i in range (0, num_steps):    
        step_wus_string = "" 
        for x in range (0, num_step_wus[i]):
            step_wus_string = step_wus_string + "wu_" + str(x)
            if (x != (num_step_wus[i] -1)):
                step_wus_string = step_wus_string + ", "
        print step_wus_string    
        config.set(section_name , "step_" + str(i), step_wus_string)   
    
    #read the resource conf file
    resource_conf_file = DARE_WD + 'tophat/input/resource.conf'
    print resource_conf_file
    resource_config = ConfigParser.ConfigParser()
    resource_config.read(resource_conf_file)                  
       
    #define resource list based upon the tasks and given input
    for i in range (0,len(resources_used)):   
        resource_conf = dict_section(resources_used[i], resource_config)
        section_name = "resource_" + str(i)
        config.add_section(section_name)        
        #constant parameters
        config.set(section_name, "resource_url", resource_conf["resource_url"] )
        config.set(section_name, "processes_per_node",  resource_conf["cores_per_node"])
        config.set(section_name, "allocation", resource_conf["allocation"]) 
        config.set(section_name, "queue", resource_conf["queue"]) 
        config.set(section_name, "bigjob_agent", resource_conf["bigjob_agent"])
        config.set(section_name, "userproxy", resource_conf["userproxy"])
        config.set(section_name, "working_directory", resource_conf["working_directory"])
        config.set(section_name, "filetransfer_url", resource_conf["filetransfer_url"])
        
        #changing parameters from job to job
        config.set(section_name, "walltime", walltime )
        config.set(section_name, "number_nodes",  number_nodes)
   
    #loop through each step
    for step in range (0, num_steps):
        
        if (step ==0):
        #add tasks for each step
            for i in range (0,num_step_wus[step]):   
                section_name = "wu_"+ str(wus_count)
                config.add_section(section_name)    
                config.set(section_name, "executable", "/bin/date")
                config.set(section_name, "number_of_processes", 1)
                config.set(section_name, "spmd_variation", "single")
                config.set(section_name, "arguments", "")
                config.set(section_name, "environment", "") 
                config.set(section_name, "working_directory", "/home/cctsg/projects/test_dare/")
                config.set(section_name, "output", "/home/cctsg/projects/test_dare/stdout.txt")
                config.set(section_name, "error", "/home/cctsg/projects/test_dare/stderr.txt")
                config.set(section_name, "appname", "simple")
                config.set(section_name, "resource" , 0)
                wus_count = wus_count + 1
        if (step ==1):
            for i in range (0,num_step_wus[step]):   
                section_name = "wu_"+ str(wus_count)
                config.add_section(section_name)    
                config.set(section_name, "executable", "/bin/date")
                config.set(section_name, "number_of_processes", 1)
                config.set(section_name, "spmd_variation", "single")
                config.set(section_name, "arguments", "")
                config.set(section_name, "environment", "") 
                config.set(section_name, "working_directory", "/home/cctsg/projects/test_dare/")
                config.set(section_name, "output", "/home/cctsg/projects/test_dare/stdout.txt")
                config.set(section_name, "error", "/home/cctsg/projects/test_dare/stderr.txt")
                config.set(section_name, "appname", "simple")
                config.set(section_name, "resource" , 0)
                wus_count = wus_count + 1
    
    #write the config file
    config.write(cfgfile)
    cfgfile.close() 
    
    os.environment
    
    #start dare
    dare_instance = dare.dare()
    dare_instance.run(conffile)
