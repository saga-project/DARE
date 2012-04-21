import time
import mimetypes
import sys
import os
import getopt
import logging
import commands
from subprocess import Popen, call, PIPE

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect, abort, Request, Response

import darehthp.model as model
import darehthp.model.meta as meta

from darehthp.lib.forms import ModelForm
from darehthp.lib.base import BaseController, render
import darehthp.lib.helpers as h


from darehthp.lib.forms_helper import  *
from darehthp.lib.modelhelper import *


from webhelpers import paginate

log = logging.getLogger(__name__)


class HthpmdController(BaseController):
    def __before__(self, action, **params):
        userid = session.get('userid')

        if userid:
            request.environ['REMOTE_USER'] = userid
            c.userid = userid
            #print "userid: %s"%user
        else:
            c.userid = "false"

        c.mess="valid"
        c.display_message =""
        c.pagenumber = ""

        jobid = session.get('jobid')
        if jobid:
            request.environ['JOBID'] = jobid
            c.jobid = jobid
        else:
            c.jobid = "none"
    #render static pages

    def index(self):
        return render('/infopages/index.mako')

    def about(self):
        return render('/infopages/about.mako')

    def resources(self):
        return render('/infopages/resources.mako')


    def software(self):
        return render('/infopages/software.mako')

    def contact(self):
        return render('/infopages/contact.mako')
    # job deletion
    def job_delete(self):
        p = c.pagenumber
        if ( p == ""):
            p = 0
        if (c.userid == "false"):
             redirect(url('/users/login?m=4'))

        jobid= request.params['id']
        #todo check whether argument given or not
        #todo check if this user has submitted this job or not

        #todo delte the running bigjob here before deleting

        del_job(jobid)
        redirect(url('/hthpmd/job_table_view?page=%s'%(p)))

    def job_table_view(self):

        user_jobs = meta.Session.query(model.job).all()

        c.jobs = paginate.Page(user_jobs, items_per_page=10)
        total_pages = len(user_jobs)/10 + 1

        # to check if user visiting this page for  the first time and
        #assign the latest jobs page,page_num tell which page to show

        page_num  =   total_pages
        if ('page' in request.params) and request.params['page']. isdigit() and (int(request.params['page']) <= total_pages):
                page_num =int(request.params['page'])

        if 'm' in request.params:
                c.display_message = "Job successfully submitted and your Job ID is " \
                + str(request.params['id'])

        c.jobs = paginate.Page(user_jobs, page=page_num, items_per_page=10)
        c.pagenums=c.jobs.pager()
        c.pagenumber = page_num
        return render("infopages/job_table_view.mako")

    def job_status_update(self):
        jobid= request.params['id']
        job_pid = get_job_pid(jobid)

        #check job is already done important

        print job_pid, "job_pid"
        if job_pid is None:
           redirect(url('/hthpmd/job_table_view'))

        if not (os.path.exists("/proc/"+str(job_pid))):
            update_job_status(jobid, "3")
            print "\n update status failed\n"

        redirect(url('/hthpmd/job_table_view'))

    #render forms
    def old_namd_form(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))
        c.form = NAMDForm()
        return render('/jobforms/old_namd_form.mako')

    def namd_form(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))
        #else:
        try:     
           action  = request.params['action']
           num = request.POST["numresources"]
           numf = request.POST["numfiles"]
           print "numf", numf
           c.form  = NAMDForm(request.POST or None, numresources=num,numfiles=numf)
        except:
           c.form  = NAMDForm(request.POST or None)
          

        return render('/jobforms/dyn_namd_form.mako')




    #for generic job submission
    def namd_job_insert(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))
        else:
        
            if request.method == 'POST':
                appname  = request.POST['appname']
                if (appname =='namd'):
                    num = request.POST["numresources"]
                    numf = request.POST["numfiles"]
                    
                    p  = NAMDForm(request.POST, request.POST ,numresources=num,numfiles=numf)
                    
                if p.is_valid():
                    #add using job queue
                    jobid =add_job(c.userid)

                    for key in p.cleaned_data:
                        #print "key", key
                        #print "value", c.form.cleaned_data[key]
                        newjobinfo = model.jobinfo()
                        newjobinfo.key = key
                        newjobinfo.value = p.cleaned_data[key]
                        newjobinfo.submitted_time = time.asctime()
                        newjobinfo.jobid = jobid
                        add_jobinfo(newjobinfo)

                    redirect(url('/hthpmd/job_table_view?m=1&id=' + str(jobid) ))
                else:
                    c.form = p
                    return render('/jobforms/dyn_namd_form.mako')
            else:
                redirect(url('/hthpmd/job_table_view'))

    # uncatogoriged
    def output_download(state):

        job_id= request.params['id']

        jobs =  meta.Session.query(model.Job).get(job_id)
        if jobs is None:
            abort(404)
        #print str(jobs.appname)

        output_filename = "NAMD_%s_output.tar.gz"%job_id

        d_path = TEMP_DATA_DIR
        abs_out_path = d_path + output_filename
        response.content_type = 'file'
        response.headers["content-type"] = "application"
        response.headers["Content-Disposition"] = "attachment;filename=%s"%output_filename
        #Mention the response headers and render the file

        if os.path.isfile(str(abs_out_path)):
            r = open(str(abs_out_path))
            return r
        else:
            redirect(url('/hthpmd/job_table_view'))

    def job_form(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))

        try:
            formtype = request.params['type']
            jobid    = request.params['jobid']
        except:
            jobid    = add_job(c.userid,"Generic Job Form")
            formtype = "resource"


        if  formtype  == "resource":

            try:
                resource_type = request.params['rtype']
                someid = request.params['sid']
                infid = add_jobmeta(jobid, formtype)

                data = {'infid': infid, 'jobid': jobid }

                if (resource_type == "pbs"):
                    c.form = pbs_resource_Form(initial=data)
                elif (resource_type == "gram"):
                    c.form = gram_resource_Form(initial=data)
                else:
                    c.form = ssh_resource_Form(initial=data)

            except:
               pass
               infid = add_jobmeta(jobid, formtype)
               data = {'infid': infid, 'jobid': jobid}
               c.form = resource_type_Form(initial=data)

        elif formtype  == "wu":
             infid = add_jobmeta(jobid, formtype)
             data = {'infid': infid, 'jobid': jobid}

             c.form = wu_Form(initial=data)

        return render('/generic_form.mako')


    def job_insert(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))

        if request.method == 'POST':

            inftype   = request.POST['inftype']
            infid     = request.POST['infid']
            jobid     = get_jobmeta_jobid(infid)

            if not (inftype == 'resource_type'):
                add_another   = request.POST['add_another']

                print "\n\n\n inftype, add_another", inftype, add_another
            else:
                resource_type = request.POST['resource_type']

            if (inftype == 'ssh_resource'):
               c.form = ssh_resource_Form(request.POST,request.POST )

            elif(inftype == 'gram_resource'):
               c.form = ssh_resource_Form(request.POST,request.POST )

            elif(inftype == 'pbs_resource'):
               c.form = ssh_resource_Form(request.POST,request.POST )

            elif(inftype == 'wu'):
               c.form = wu_Form(request.POST,request.POST )

            else:
               c.form = resource_type_Form(request.POST,request.POST )

            if c.form.is_valid():
                #add using job queue
                for key in c.form.cleaned_data:
                    if (key == "infid") or (key == "jobid")or (key == "someid"):
                        continue
                    add_jobinfo(key,c.form.cleaned_data[key], infid)


                if (inftype == 'resource_type'):
                    redirect(url("/hthpmd/job_form",type="resource",jobid =str(jobid),\
                         rtype=str(resource_type), sid=str(infid)))

                elif (inftype == 'wu'):
                    if add_another == "false":
                        update_job_status(jobid, str(JOBSTATES.NEW))
                        redirect(url("/hthpmd/job_table_view?m=1&id=" + str(jobid)))
                    else:
                        redirect(url("/hthpmd/job_form",type="wu",jobid =str(jobid)  ))
                else:
                    if add_another == "false":
                        redirect(url("/hthpmd/job_form",type="wu",jobid =str(jobid)  ))
                    else:
                        redirect(url("/hthpmd/job_form",type="resource",jobid =str(jobid)  ))

            else:
                return render('/generic_form.mako')




