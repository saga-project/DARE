import os
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import redirect

import darecactus.model as model
import darecactus.model.meta as meta

from darecactus.lib.base import BaseController, render

from darecactus.lib.cactusormhelper import *
from darecactus.lib.cactusformshelper import *

# pagination
from webhelpers import paginate


einstientoolkit_file = os.path.join(os.path.abspath('.'), '..', 'lib', 'DARE', 'examples', 'cactus', 'einsteintoolkit.th')

log = logging.getLogger(__name__)


class CactusController(BaseController):

    def __before__(self, action, **params):
        userid = session.get('userid')
        if userid:
            request.environ['REMOTE_USER'] = userid
            c.userid = userid
            #print "userid: %s"%user
        else:
            c.userid = "false"
        c.mess = "valid"
        c.display_message = ""
        c.pagenumber = ""

    def index(self):
        return render('/pages/index.mako')

    def about(self):
        return render('/pages/about.mako')

    def using_cactus(self):
        return render('/pages/using_cactus.mako')

    def upload_thorn(self):
        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=upload_thorn'))
        c.form = ThornForm()
        return render('/forms/thorn_form.mako')

    def thorn_list(self):

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=thorn_list'))

        thornlist = get_thornlist(c.userid)

        total_pages = len(thornlist) / 10 + 1

        #jobs = meta.Session.query(model.job)
        #if (len(user_jobs)!=0):
         #   print "\njobs------\n", jobs.first().jobinfo[1].key,jobs.first().jobinfo[1].value

        # to check if user visiting this page for  the first time and
        #assign the latest jobs page,page_num tell which page to show

        page_num = total_pages

        c.thornlist = paginate.Page(thornlist, page=page_num, items_per_page=10)
        c.pagenums = c.thornlist.pager()
        c.pagenumber = page_num

        return render('/pages/thorn_list.mako')

    def save_thorn(self):
        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=save_thorn'))

        if request.method == 'POST':
            thornfile = request.POST['thornfile']
            thornform = ThornForm(request.POST)
            if thornform.is_valid():
                add_thorn(c.userid,  thornform.cleaned_data['description'], thornfile)
                redirect(url('/cactus/thorn_list'))
            else:
                c.form = thornform
                return render('/forms/thorn_form.mako')

    def download_thorn(self):

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=download_thorn'))

        thornid = request.params['id']
        if thornid == 'default':
            thornname = 'einsteintoolkit.th'
            thornfile = file(einstientoolkit_file)
        else:
            thornname, thornfile = get_thorn(thornid)

        response.headers["content-type"] = "application"
        response.headers["Content-Disposition"] = "attachment;filename=%s" % thornname

        return thornfile

    def param_list(self):
        return render('/pages/param_list.mako')

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
        if (p == ""):
            p = 0

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=job_delete'))

        jobid = request.params['id']

        del_job(jobid)
        redirect(url('/cactus/job_table_view?page=%s' % (p)))

    def cactus_form(self):
        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=cactus_form'))

        thorns = get_thornlist_job(c.userid)

        c.form = CactusForm(thorns=thorns)

        return render('/forms/cactus_form.mako')

    def job_insert(self):

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=cactus_form'))

        thorns = get_thornlist_job(c.userid)
        if request.method == 'POST':

            try:
                paramfile = request.POST['parameterfile']
                print 'thornfile.filename', paramfile.filename
                #print 'thornfile.filename', paramfile.file.read()
                param_exists = True
            except:
                param_exists = False

            data_form = CactusForm(request.POST, thorns=thorns)

            if data_form.is_valid() and param_exists:
                #add using job queue
                jobid = add_job(c.userid)

                add_allnewjobinfo(data_form.cleaned_data, jobid)
                add_param(paramfile, jobid)

                #import pdb; pdb.set_trace()
                redirect(url('/cactus/job_table_view?m=1&id=' + str(jobid)))
            else:

                c.form = data_form
                c.form.fields['thornlist'].choices = thorns
                return render('/forms/cactus_form.mako')

        #        redirect(url('/cactus/job_table_view'))

    def job_table_view(self):

        user_jobs = meta.Session.query(model.job).all()

        c.jobs = paginate.Page(user_jobs, items_per_page=10)
        total_pages = len(user_jobs) / 10 + 1

        #jobs = meta.Session.query(model.job)
        #if (len(user_jobs)!=0):
         #   print "\njobs------\n",jobs.first().jobinfo[1].key, jobs.first().jobinfo[1].value

        # to check if user visiting this page for  the first time and
        #assign the latest jobs page,page_num tell which page to show

        page_num = total_pages
        if ('page' in request.params) and request.params['page'].isdigit() and (int(request.params['page']) <= total_pages):
                page_num = int(request.params['page'])

        if 'm' in request.params:
                c.display_message = "Job successfully submitted and your Job ID is " \
                + str(request.params['id'])

        c.jobs = paginate.Page(user_jobs, page=page_num, items_per_page=10)
        c.pagenums = c.jobs.pager()
        c.pagenumber = page_num
        return render("/pages/job_table_view.mako")

    def download_job_input(self):

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=download_thorn'))

        jobid = request.params['jobid']
        file_type = request.params['type']

        outname, outfile = get_job_file(jobid, file_type)
        print 'outname, outfile ', outname, outfile

        response.headers["content-type"] = "application"
        response.headers["Content-Disposition"] = "attachment;filename=%s" % outname

        return outfile

    def download_job_output(self):

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=download_thorn'))
        try:
            jobid = request.params['jobid']
        except:
            return "jobid does not exist"
        filepath = os.path.join(os.getenv('HOME'), "DAREJOBS", "darecactus", str(jobid), "%s-cactus.tar.gz" % jobid)

        if os.path.isfile(filepath):
            outfile = open(filepath, 'r')
            response.headers["content-type"] = "application"
            response.headers["Content-Disposition"] = "attachment;filename=%s-cactus.tar.gz" % jobid
            return outfile
        else:
            return "file does not exist"

    def job_status_update(self):

        if (c.userid == "false"):
            redirect(url('/users/login?cont=cactus&action=job_status_update'))

        jobid = request.params['id']
        job_pid = get_job_pid(jobid)

        #check job is already done important

        print job_pid, "job_pid"
        if job_pid is None:
            redirect(url('/cactus/job_table_view'))

        if not (os.path.exists("/proc/" + str(job_pid))):
            update_job_status(jobid, "3")
            print "\n update status failed\n"

        redirect(url('/cactus/job_table_view'))
