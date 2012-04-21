import os
import sys
import time
import ConfigParser
import uuid
#import dare
import optparse


"""

major change log 
moving dict_section to dare.py
change the dict_section(job_config, "JOB") to section name 2nd argument
steps staring point (0 or 1?)
config to dare_config
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
    
    DARE_HOME = job_config.get('JOB', "dare_home")       
    
    os.environ["DARE_HOME"]=DARE_HOME

    sys.path.insert(0, DARE_HOME)
    try:
        from dare import dict_section, dare
    except:
        print "failed to import dare"
        sys.exit(0)
    job_conf = dict_section( job_config, "JOB")
       
    #print job_conf
    #get the resources used from job configuration file
    job_size = job_conf["job_size"]
    
    if (job_size == "small" ):
       resources_used = ["cyder"]
    elif (job_size == "medium" ):
       resources_used = ["eric"] 
    elif (job_size == "Large" ):
       resources_used = ["qb"]       
    elif (job_size == "cloud" ):
       resources_used = ["aws"]     
    jobid = job_conf["jobid"] 
    
    #get the dare_cwd
    DARE_HOME = job_conf["dare_home"]       
    colorspace = job_conf["colorspace"]
    
    
    #TODO calculate number of nodes an walltime here now its static
    number_nodes = [1] 
    walltime  = [100]    
    
    #application working directory
    working_directory = os.path.join(DARE_HOME, "darefiles/", str(jobid)) 
    
    #start building the dare conf file for dare
    dare_config = ConfigParser.ConfigParser()

    control_input = job_conf["control_input_name"]
    control_input_name = control_input.split(".fastq")[0]
    treat_input = job_conf["treat_input_name"]
    treat_input_name = treat_input.split(".fastq")[0]
    
    #input_list = [job_conf["input_list"].split(",")]
    input_list = [treat_input,control_input]
    input_list_names =[]
    for i in range(0, len(input_list)):
        input_list_names.append(str(input_list[i].split(".fastq")[0]) + "_" + str(i))
        
###################################################################################################
##########          define resource list                        ###################################
###################################################################################################

    #read the resource conf file
    resource_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/resource.cfg')
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
    
    """    
###################################################################################################
##########          step =0(data)         ######################################################
###################################################################################################
    
    step = 0
    num_step_wus[step]= 2
    step_type[step] = "data"    
##########          wu_0       ######################################################
 
    section_name = "wu_"+ str(wus_count)
    dare_config.add_section(section_name)    
    dare_config.set(section_name, "appname", "file_transfer")
    dare_config.set(section_name, "fs_type", "scp")
    dare_config.set(section_name, "source_url", os.path.join(DARE_HOME, "chipseq/user_input" ,control_input))
    dare_config.set(section_name, "dest_url", "cctsg@cyder.cct.lsu.edu:" + os.path.join(working_directory))    
    wus_count = wus_count + 1
##########          wu_0       ######################################################

    section_name = "wu_"+ str(wus_count)
    dare_config.add_section(section_name)    
    dare_config.set(section_name, "appname", "file_transfer")
    dare_config.set(section_name, "fs_type", "scp")
    dare_config.set(section_name, "source_url", os.path.join(DARE_HOME, "chipseq/user_input" ,treat_input))
    dare_config.set(section_name, "dest_url", "cctsg@cyder.cct.lsu.edu:" + os.path.join(working_directory))    
    wus_count = wus_count + 1
    """

###################################################################################################
##########          step =0(data)         ######################################################
###################################################################################################

    #following line mandotory for each step
    step =0 
    num_step_wus[step]= 2
    step_type[step] = "compute"
    
    #add tasks for each step

##########          wu_0        ######################################################
    for i in range(0,len(input_list_names)):
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)

        dare_config.set(section_name, "executable", "/bin/ln")
        dare_config.set(section_name, "number_of_processes","2")
        dare_config.set(section_name, "spmd_variation", "single")
        dare_config.set(section_name, "arguments",  os.path.join(DARE_HOME, "examples/chipseq/user_input", input_list[i]) +" "+ os.path.join(working_directory, input_list_names[i] ) )
        dare_config.set(section_name, "environment", "")
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "linking")
        dare_config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1


###################################################################################################
##########          step =1 (compute)         ######################################################
###################################################################################################

    #following line mandotory for each step
    step = 1
    num_step_wus[step]= 2
    step_type[step] = "compute"
    
    
    
    #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/chipseq_1_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    if (colorspace == "true"):
         args = "arguments"
    else:
         args = "arguments_1"
    print "step_resource_conf", step_resource_conf["ngsdata"]     
    if (job_conf["reference_genome"] == "ws200"):
       ref_fa = os.path.join(step_resource_conf["ngsdata"], "GENOME_DATABASE/NEMATODE/ws200/bwa/ILLUMINA/c_elegnas_ws200_dna")
    
    elif (job_conf["reference_genome"] == "mm9"):
       ref_fa = os.path.join(step_resource_conf["ngsdata"], "GENOME_DATABASE/MOUSE/mm9/chr19/bwa/SOLID/chr19.fa")
    else:
       ref_fa = os.path.join(step_resource_conf["ngsdata"], "GENOME_DATABASE/MOUSE/mm9/chr19/bwa/SOLID/chr19.fa")

       
   #for loop to all tasks
##########          wu_1        ######################################################
    for i in range(0,len(input_list_names)):
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
            
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf[args] +" "\
              + ref_fa + " "\
              + os.path.join(working_directory, input_list_names[i] + ".fastq")+ " > "\
              + os.path.join(working_directory, input_list_names[i] + ".sai") )
              
        dare_config.set(section_name, "environment", step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1


    
####################################################################################################
##########          step =2 (compute)         ######################################################
####################################################################################################
     
    step = 2
    num_step_wus[step]= 2
    step_type[step] = "compute"
        
    #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/chipseq_2_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    
##########          wu_3        ######################################################
    for i in range(0,len(input_list_names)):
    
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
            
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf["arguments"] +" "\
            + ref_fa + " "\
            + os.path.join(working_directory, input_list_names[i] +".sai")+ " " \
            + os.path.join(working_directory, input_list_names[i] + ".fastq") + " > "\
            + os.path.join(working_directory, input_list_names[i] +".sam")  
            )
        dare_config.set(section_name, "environment", step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1



####################################################################################################
##########          step =3 (compute)         ######################################################
####################################################################################################
     
    step = 3
    num_step_wus[step]= 2
    step_type[step] = "compute"

    #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/chipseq_3_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    
##########          wu_5       ######################################################
    for i in range(0,len(input_list_names)):       
        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
            
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf["arguments"] +" "\
            + os.path.join(working_directory, input_list_names[i] +".sam") 
            +  " > " + os.path.join(working_directory, input_list_names[i] +".bam")  
            )
        dare_config.set(section_name, "environment", step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1


####################################################################################################
##########          step =4 (compute)         ######################################################
####################################################################################################
     
    step = 4
    num_step_wus[step]= 2
    step_type[step] = "compute"
    
        #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/chipseq_4_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    
##########          wu_7      ######################################################
    for i in range(0,len(input_list_names)):       

        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
            
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf["arguments"] +" "\
            + os.path.join(working_directory, input_list_names[i] +".bam") 
            + " " + os.path.join(working_directory, input_list_names[i] +"-sorted")  
            )
        dare_config.set(section_name, "environment", step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1  

    
####################################################################################################
##########          step =5 (compute)         ######################################################
####################################################################################################
     
    step = 5
    num_step_wus[step]= 2
    step_type[step] = "compute"    
    
    #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/chipseq_5_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    
##########          wu     ######################################################
    for i in range(0,len(input_list_names)):       

        section_name = "wu_"+ str(wus_count)
        dare_config.add_section(section_name)    
        dare_config.set(section_name, "executable", step_conf["executable"])
        dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
        dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
        dare_config.set(section_name, "arguments", step_resource_conf["arguments"] +" "\
            + os.path.join(working_directory, input_list_names[i]  +".-sorted.bam")  
            )
        dare_config.set(section_name, "environment", step_resource_conf["environment"]) 
        dare_config.set(section_name, "working_directory", working_directory)
        dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
        dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
        dare_config.set(section_name, "appname", "simple")
        dare_config.set(section_name, "resource" , 0)
        wus_count = wus_count + 1   


    
####################################################################################################
##########          step =6 (compute)         ######################################################
####################################################################################################
     
    step = 6
    num_step_wus[step]= 1
    step_type[step] = "compute"    
    
    #add tasks for each step
    step_conf_file = os.path.join(DARE_HOME, 'examples/chipseq/chipseq_6_resource.cfg')
    step_config = ConfigParser.ConfigParser()
    step_config.read(step_conf_file) 
    step_conf = dict_section( step_config, "common")
    step_resource_conf = dict_section(step_config, resources_used[0])
    
##########          wu     ######################################################
    section_name = "wu_"+ str(wus_count)
    dare_config.add_section(section_name)    
    dare_config.set(section_name, "executable", step_conf["executable"])
    dare_config.set(section_name, "number_of_processes", step_conf["number_of_processes"])
    dare_config.set(section_name, "spmd_variation", step_conf["spmd_variation"])
    dare_config.set(section_name, "arguments", " -t "\
        + os.path.join(working_directory, input_list_names[0] +"-sorted.bam")   +" -c "\
        + os.path.join(working_directory, input_list_names[1]+"-sorted.bam") + " " +step_resource_conf["arguments"] 
        )
    dare_config.set(section_name, "environment", step_resource_conf["environment"]) 
    dare_config.set(section_name, "working_directory", working_directory)
    dare_config.set(section_name, "output", os.path.join(working_directory, "stdout-"+ str(dare_uuid) +"-"+str(wus_count)+".txt"))
    dare_config.set(section_name, "error", os.path.join(working_directory, "stderr-"+ str(dare_uuid) +"-"+str(wus_count)+".txt" ))
    dare_config.set(section_name, "appname", "simple")
    dare_config.set(section_name, "resource" , 0)
    wus_count = wus_count + 1      
    # we have the number of tasks per each step and resource list at this point


###################################################################################################
##########    finally      define DAREJOB  for dare.py   ##########################################
###################################################################################################    
    
    section_name = 'DAREJOB'
    dare_config.add_section(section_name)
    dare_config.set(section_name, "jobid", jobid) 
    dare_config.set(section_name, "num_resources", len(resources_used)) 
    dare_config.set(section_name, "updatedb", "true") 
    
    dare_config.set(section_name, "num_steps", len(num_step_wus)) 
    dare_config.set(section_name, "log_filename", os.path.join(working_directory, str(jobid) +"-dummy-darelog.txt"))
    
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
