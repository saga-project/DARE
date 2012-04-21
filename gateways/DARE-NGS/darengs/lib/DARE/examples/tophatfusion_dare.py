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
    parser.add_option("-c", "--conf_job", dest="conf_job", help="job configuration file")
    (options, args) = parser.parse_args()


    job_config = ConfigParser.ConfigParser()
    confjob = options.conf_job
    job_config.read(confjob)
    job_conf = dict_section("JOB", job_config)
    
    #print job_conf
    #get the resources used from job configuration file   
    resources_used = [job_conf["machine"]]
    jobid = job_conf["jobid"] 
    #get the dare_cwd
    DARE_DIR = job_conf["dare_dir"]       
    
    
    #calculate number of nodes an walltime here now its static
    number_nodes = [1] 
    walltime  = [100]
     
    #application specific important for building a workflow
    #add tasks here
    num_step_wus = [1,2,1,1]
    
    #application working directory
    working_directory = os.path.join(DARE_DIR, "darefiles/", str(jobid)) 
    #print working_directory
    #os.system("mkdir -p "+ working_directory) 

    #start building the conf file for dare
    dare_conffile =  os.path.join(working_directory, str(jobid) +"-darejob.cfg") 
    config = ConfigParser.ConfigParser()
    cfgfile = open(dare_conffile,'w')
    
    #add most important section here
    section_name = 'DAREJOB'
    config.add_section(section_name)
    config.set(section_name , "jobid", jobid) 
    config.set(section_name , "num_resources", len(resources_used)) 
    config.set(section_name , "num_steps", len(num_step_wus)) 
    #define the file transfer steps
    config.set(section_name , "ft_steps", "step_1,step_3") 
    config.set(section_name , "log_filename", os.path.join(working_directory, str(jobid) +"-darelog.txt"))
    wus_count = 0
    
    for i in range (0, len(num_step_wus)):    
        step_wus_string = "" 
        for x in range (0, num_step_wus[i]): 
            step_wus_string = step_wus_string + "wu_" + str(wus_count)
            if (x != (num_step_wus[i] -1)):
                step_wus_string = step_wus_string + ", "
            wus_count = wus_count + 1
        print step_wus_string    
        config.set(section_name , "step_" + str(i), step_wus_string)   
    
    #read the resource conf file
    resource_conf_file = os.path.join(DARE_DIR, 'tophatfusion/resource.cfg')
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
        config.set(section_name, "working_directory", working_directory)
        config.set(section_name, "filetransfer_url", resource_conf["filetransfer_url"])
        
        #changing parameters from job to job
        config.set(section_name, "walltime", walltime[i])
        config.set(section_name, "number_nodes",  number_nodes[i])
  
    wus_count = 0 
    #loop through each step
        
    step =0
    
    #add tasks for each step
    step_conf_file = os.path.join(DARE_DIR, 'tophatfusion/tophatfusion_1_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section("common", step_config)
    step_resource_conf = dict_section(resources_used[0], step_config)
    
    for i in range (0, num_step_wus[step]):   
        section_name = "wu_"+ str(wus_count)
        config.add_section(section_name)    
        """
        config.set(section_name, "executable", step_conf["executable"])
        config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        config.set(section_name, "arguments", "-o "+ working_directory + "/tophat_MCF7 "+ step_resource_conf["arguments"] )
        config.set(section_name, "environment", step_resource_conf["environment"]) 
        config.set(section_name, "working_directory", working_directory)
        config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        config.set(section_name, "appname", "simple")
        config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1
        """
        config.set(section_name, "executable", "/bin/date")
        config.set(section_name, "number_of_processes", 1)
        config.set(section_name, "spmd_variation", "single")
        config.set(section_name, "arguments", "")
        config.set(section_name, "environment","") 
        config.set(section_name, "working_directory", working_directory)
        config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        config.set(section_name, "appname", "simple")
        config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1
        
    #step to copy files
    
    step = step + 1
       
    
    #dummy ft
    
    section_name = "wu_"+ str(wus_count)
    config.add_section(section_name)    
    config.set(section_name, "appname", "file_transfer")
    config.set(section_name, "fs_type", "scp")
    config.set(section_name, "source_url", DARE_DIR+"/darefiles/output_dare/27/tophat_MCF7/")
    config.set(section_name, "dest_url", "cctsg@cyder.cct.lsu.edu:" + working_directory)    
    wus_count = wus_count + 1
   
    section_name = "wu_"+ str(wus_count)
    config.add_section(section_name)    
    config.set(section_name, "appname", "file_transfer")
    config.set(section_name, "fs_type", "scp")
    config.set(section_name, "source_url", "/home/cctsg/jhkim/tophat-fusion-test/*")
    config.set(section_name, "dest_url", "cctsg@cyder.cct.lsu.edu:" + working_directory)    
    wus_count = wus_count + 1

    
    step = step + 1
    
    #adding step conf file into dict
    step_conf_file = os.path.join(DARE_DIR, 'tophatfusion/tophatfusion_2_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section("common", step_config)
    step_resource_conf = dict_section(resources_used[0], step_config)
    
    for i in range (0, num_step_wus[step]):   
        section_name = "wu_"+ str(wus_count)
        config.add_section(section_name)    
        #comment from here
        config.set(section_name, "executable", step_conf["executable"])
        config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        config.set(section_name, "arguments", step_resource_conf["arguments"] )
        config.set(section_name, "environment", step_resource_conf["environment"]) 
        config.set(section_name, "working_directory", working_directory)
        config.set(section_name, "output", os.path.join(working_directory,  "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        config.set(section_name, "error", os.path.join(working_directory,  "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        config.set(section_name, "appname", "simple")
        config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1  
        """
        config.set(section_name, "executable", "/bin/date")
        config.set(section_name, "number_of_processes", 1)
        config.set(section_name, "spmd_variation", "single")
        config.set(section_name, "arguments", "")
        config.set(section_name, "environment","") 
        config.set(section_name, "working_directory", working_directory)
        config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        config.set(section_name, "appname", "simple")
        config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1
        """
    step = step + 1
       
    
    # ft after result. html
    
    section_name = "wu_"+ str(wus_count)
    config.add_section(section_name)    
    config.set(section_name, "appname", "file_transfer")
    config.set(section_name, "fs_type", "scp")
    config.set(section_name, "source_url", working_directory + "/tophatfusion_out/result.html")
    config.set(section_name, "dest_url",  "cctsg@cyder.cct.lsu.edu:" +"/home/cctsg/install/DARE-NGS/darengs/templates/tophat_results/result_"+ jobid+ ".mako"  )    
    wus_count = wus_count + 1    
        
    #write the config file
    config.write(cfgfile)
    cfgfile.close() 
    
    
    #start dare with above written config file
    dare_instance = dare.dare()
    dare_instance.run(dare_conffile)

    