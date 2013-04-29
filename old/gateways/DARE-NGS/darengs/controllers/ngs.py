import time
import mimetypes
import sys
import os
import getopt
import logging
import commands
from subprocess import Popen, call, PIPE

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import darengs.model as model
import darengs.model.meta as meta

from darengs.lib.forms import ModelForm
from darengs.lib.base import BaseController, render
import darengs.lib.helpers as h


from darengs.lib.ModelHelper import *
from darengs.lib.forms_helper import  bfastForm, tophatfusionForm, chipseqForm


# pagination
from webhelpers import paginate

log = logging.getLogger(__name__)



class NgsController(BaseController):

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
    def index(self):

        return render('/pages/index.mako')


    def about(self):
        return render('/pages/about.mako')

    def using_chipseq(self):
        return render('/pages/using_chipseq.mako')

    def using_tophatfusion(self):
        return render('/pages/using_tophatfusion.mako')

    def using_bfast(self):
        return render('/pages/using_bfast.mako')


    def resources(self):
        return render('/pages/resources.mako')

    def trac(self):
        return render('/pages/trac.mako')

    def software(self):
        return render('/pages/software.mako')

    def contact(self):
        return render('/pages/contact.mako')

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
        print request.url
        redirect(url('/ngs/job_table_view?page=%s'%(p)))

    #todo merge the three forms into one and use parameters
    def bfast_form(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))
        c.form = bfastForm()
        return render('/forms/bfast_form.mako')

    def tophatfusion_form(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))
        c.form = tophatfusionForm()
        return render('/forms/tophatfusion_form.mako')

    def chipseq_form(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))
        c.form = chipseqForm()
        return render('/forms/chipseq_form.mako')

    def dalliance(self):
        """ dalliance visual"""
        return render('/dalliance.mako')

    def tophatfusion_view(self):
        """ dalliance visual"""
        jobid= request.params['id']
        if jobid is None:
           redirect(url('/ngs/job_table_view'))
        return render('/results/result_'+ jobid+'.mako')

    def job_insert(self):
        if (c.userid == "false"):
             redirect(url('/users/login?m=1'))

        #extra_questions = get_questions(request)
        #form = UserCreationForm(request.POST or None, extra=extra_questions)

        if request.method == 'POST':
            appname  = request.POST['appname']
            if (appname =='tophatfusion'):
               c.form = tophatfusionForm(request.POST,request.POST )
            elif (appname =='bfast') :
               c.form = bfastForm(request.POST,request.POST )
            elif (appname =='chipseq') :
               c.form = chipseqForm(request.POST,request.POST )

            if c.form.is_valid():
                #add using job queue
                jobid =add_job(c.userid)

                for key in c.form.cleaned_data:
                    print "key", key
                    print "value", c.form.cleaned_data[key]
                    newjobinfo = model.jobinfo()
                    newjobinfo.key = key
                    newjobinfo.value = c.form.cleaned_data[key]
                    newjobinfo.submitted_time = time.asctime()
                    newjobinfo.jobid = jobid
                    add_jobinfo(newjobinfo)

                update_job_status(jobid, str(JOBSTATES.NEW))
                redirect(url('/ngs/job_table_view?m=1&id=' + str(jobid) ))
            else:
                return render('/forms/chipseq_form.mako')
        #        redirect(url('/ngs/job_table_view'))

    def job_table_view(self):

        user_jobs = meta.Session.query(model.job).all()

        c.jobs = paginate.Page(user_jobs, items_per_page=10)
        total_pages = len(user_jobs)/10 + 1

        #jobs = meta.Session.query(model.job)
        #if (len(user_jobs)!=0):
         #   print "\njobs------\n",jobs.first().jobinfo[1].key, jobs.first().jobinfo[1].value

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
        return render("/job_table_view.mako")

    def job_status_update(self):

        jobid= request.params['id']
        job_pid = get_job_pid(jobid)

        #check job is already done important

        print job_pid, "job_pid"
        if job_pid is None:
           redirect(url('/ngs/job_table_view'))

        if not (os.path.exists("/proc/"+str(job_pid))):
            update_job_status(jobid, "3")
            print "\n update status failed\n"

        redirect(url('/ngs/job_table_view'))

    def output_download(state):
        t =0
        job_id= request.params['id']
        t= request.params['t']
        if int(t) == 2:
            output_filename = "test_peaks.xls"
        else:
            output_filename = "out_peaks.bed"

        output_dir = "/home/cctsg/software/DARE-NGS/darengs/lib/DARE/darefiles/%s/"%job_id


        response.content_type = 'file'
        response.headers["content-type"] = "application"
        response.headers["Content-Disposition"] = "attachment;filename=%s"%(output_filename)
        #Mention the response headers and render the file

        if os.path.isfile(output_dir + output_filename):
            r = open(output_dir +output_filename)
            return r
        else:
            redirect(url('/ngs/job_table_view'))
