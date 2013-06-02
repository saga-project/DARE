from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.template import RequestContext
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from .models import Job, UserContext, UserResource, UserTasks, JobInfo, UserPilots, DareBigJob, DareBigJobTask, DareBigJobPilot, simple_task_script , DefaultDareBigJobPilot
from .forms import UserContextTable, UserContextForm, UserResourceTable, UserResourceForm, UserPilotsForm, UserTasksForm
from .forms import PilotForm, ResourceEditConf, BigJobForm, PilotPopup
from .tasks import start_pilot, stop_pilot, get_pilot_status, start_task, get_task_status
import simplejson as json


DEFAULT_PILOTS = {'stampede': {"service_url": 'slurm+ssh://smaddi2@ranger.tacc.utexas.edu',
                     "number_of_processes": 16,
                     "queue": "development",
                     "walltime": 10,
                     "allocation": "TG-MCB090174",
                     "working_directory": "/work/01395/smaddi2/dare/",
                    },
                 'lonestar':  {"service_url": 'sge+ssh://smaddi2@lonestar.tacc.utexas.edu',
                     "number_of_processes": 16,
                     "queue": "development",
                     "walltime": 10,
                     "allocation": "TG-MCB090174",
                     "working_directory": "/work/01395/smaddi2/dare/",
                    }
            }

DEFAULT_PILOT_VALS = {"service_url": 'fork://localhost',
                     "number_of_processes": 1,
                     "queue": "development",
                     "walltime": 10,
                     "allocation": "TG-MCB090174",
                     "working_directory": "/work/01395/smaddi2/dare/",
                    }


def view_home(request):
    return render(request, 'static/home.html')


def view_static(request, page_type):
    template = 'static/%s.html' % page_type
    return render(request, template)


def view_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You're successfully logged in!")
            else:
                messages.success(request, "Your account is not active, please contact the site admin.")
            return HttpResponseRedirect("/")
        else:
            messages.success(request, "Your username and/or password were incorrect.")

    return render_to_response('static/login_form.html', context_instance=RequestContext(request))


def view_login_all(request):
    """Logs out user"""
    page_type = "login"
    template = 'static/%s.html' % page_type
    return render(request, template)


def view_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect("/dashboard/")


def view_logout(request):
    """Logs out user"""
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def view_manage_contexts(request):
    if request.method == 'POST':
        form = UserContextForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            form = UserContextForm()
    else:
        form = UserContextForm()
    context = {}
    queryset = UserContext.objects.filter(user=request.user)
    context['table'] = UserContextTable(queryset)
    context['form'] = form

    return render_to_response("darewap/context_form.html", context, context_instance=RequestContext(request))


@login_required
def view_manage_resources(request):
    if request.method == 'POST':
        form = UserResourceForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            form = UserResourceForm()
    else:
        form = UserResourceForm()
    context = {}
    queryset = UserResource.objects.filter(user=request.user)
    context['table'] = UserResourceTable(queryset)
    context['form'] = form

    return render_to_response("darewap/context_form.html", context, context_instance=RequestContext(request))


@login_required
def view_job_list(request):
    jobs = Job.objects.filter(user=request.user).order_by('-modified')
    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        jobs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        jobs = paginator.page(paginator.num_pages)
    # Render list page with the documents and the form
    return render_to_response('darewap/job_table_view.html', {'jobs': jobs}, context_instance=RequestContext(request))


@login_required
def view_job_actions(request):
    job_id = request.GET.get('job_id')
    action = (str(request.GET.get('action'))).strip()
    if job_id:
        job = Job.objects.filter(id=job_id, user=request.user)[0]
        if action == 'delete':
            job.delete()
            return render_to_response('darewap/job_actions.html', {'message': 'Job %s Deleted' % job_id}, context_instance=RequestContext(request))
        else:
            return render_to_response('darewap/job_actions.html', {'job': job}, context_instance=RequestContext(request))

    else:
        return render_to_response('darewap/job_actions.html', {'message': 'Job not found'}, context_instance=RequestContext(request))


@login_required
def view_create_job_bigjob(request):
    if request.method == 'POST':
        form = PilotForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            job = form.save(request)
            start_pilot(job)
            return HttpResponseRedirect('/job/tasks/')
            #messages.success(request, "Job Succesfully created")
        else:
            messages.error(request, "Error in creating job: Inavlid Form")
    else:
        job = Job(user=request.user, status="New")
        job.save()
        form = PilotForm(request.user)

    #import pdb;pdb.set_trace()
    return render_to_response('darewap/create_job_pilot.html', {'form': form, 'job_id': job.id}, context_instance=RequestContext(request))


@login_required
def view_create_tasks(request):
    #if request.method == 'POST':
        #print "submitted"
        #form = TaskForm(request.user, request.POST, request.FILES)
        #if form.is_valid():
        #    form.save(request)
            #messages.success(request, "Job Succesfully created")
        #else:
        #    messages.error(request, "Error in creating job: Inavlid Form")
    #else:
        #form = TaskForm(request.user)
    return render_to_response('darewap/create_tasks.html', context_instance=RequestContext(request))


@login_required
def view_resource_edit_conf(request, job_id, pilot):
    if request.method == 'POST':
        form = ResourceEditConf(request.user, request.POST, request.FILES, job_id=job_id, pilot=pilot)
        print form.is_valid(), form.errors
        if form.is_valid():
            form.save(request)
            #messages.success(request, "Job Succesfully created")
        else:
            messages.error(request, "Error in creating job: Inavlid Form")
    else:
        form = ResourceEditConf(request.user, job_id=job_id, pilot=pilot)
    return render_to_response('darewap/resource_edit_conf.html', {'form': form, 'pilot': pilot, 'job_id': job_id}, context_instance=RequestContext(request))


@login_required
def view_job_tasks(request):
    form = None
    mytasks = UserTasks.objects.filter(user=request.user)
    return render_to_response('darewap/create_job_tasks.html', {'form': form, 'tasks': mytasks}, context_instance=RequestContext(request))


@login_required
def view_manage_tasks(request):

    if request.GET.get('del') == 'true':
        tid = request.GET.get('id')
        try:
            ll = UserTasks.objects.get(id=tid)
            ll.delete()
        except:
            messages.failure(request, "Task Succesfully Deleted")
        return HttpResponseRedirect("/my-tasks/")

    if request.GET.get('new') == 'true':
        form = UserTasksForm()
        return render_to_response('darewap/tasks/new_task_script.html', {'form': form},  context_instance=RequestContext(request))

    if request.GET.get('edit') == 'true':
        tid = request.GET.get('id')
        try:
            task = UserTasks.objects.get(id=tid)
        except:
            task = None
        if task:
            form = UserTasksForm(instance=task)
            return render_to_response('darewap/tasks/new_task_script.html', {'form': form, 'tid': tid},  context_instance=RequestContext(request))

    if request.method == 'POST':

        tid = request.GET.get('id')
        form = None
        if tid:
            try:
                task = UserTasks.objects.get(id=tid)
            except:
                task = None
            if task:
                form = UserTasksForm(request.POST, request.FILES, instance=task)
        if not form:
            form = UserTasksForm(request.POST, request.FILES)

        #import pdb;pdb.set_trace()
        if form.is_valid():
            task = form.save(request=request)
            messages.success(request, "Task Succesfully Saved")
            return render_to_response('darewap/tasks/new_task_script.html', {'form': form, 'tid': task.id},  context_instance=RequestContext(request))
        else:
            return render_to_response('darewap/tasks/new_task_script.html', {'form': form},  context_instance=RequestContext(request))

    mytasks = UserTasks.objects.filter(user=request.user)
    return render_to_response('darewap/tasks/manage_tasks.html', {'mytasks': mytasks}, context_instance=RequestContext(request))


@login_required
def view_bigjob(request):

    if request.GET.get('del') == 'true':
        job_id = request.GET.get('job_id')
        try:
            ll = Job.objects.get(id=job_id)
            ll.delete()
            messages.success(request, "Job Succesfully Deleted with %s " % job_id)
        except:
            messages.success(request, "Job Deletion Failed- id=%s" % job_id)
        return HttpResponseRedirect("/view-job-list/")

    if request.method == 'POST':
        form = BigJobForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            job = form.save(request)
            return HttpResponseRedirect('/job/tasks/')
            messages.success(request, "Job Title Succesfully Saved")
        else:
            messages.error(request, "Error in creating job: Inavlid Form")
            retrun_dict = {}
    else:
        job_id = request.GET.get('job_id')
        if job_id:
            if  not request.GET.get('action'):
                job = Job.objects.get(id=job_id)
                bigjobform = BigJobForm(request.user, instance=job)
                pilotform = PilotForm(request.user)
                mytasks = UserTasks.objects.filter(user=request.user)
                jobtasks = JobInfo.objects.filter(job=job, itype='task')
                #if len(jobtasks) < 1:
                #    job.create_task()
                #    jobtasks = JobInfo.objects.filter(job=job, itype='task')

                retrun_dict = {'bigjobform': bigjobform, "pilotform": pilotform, 'job_id': job.id, "mytasks": mytasks, 'jobtasks': jobtasks}
                return render_to_response('darewap/bigjob/main.html', retrun_dict, context_instance=RequestContext(request))

            elif str(request.GET.get('action')) == "create_task":
                print request.GET.get('action'), request.GET.get('job_id'), str(request.GET.get('action')) == "create_task"

                jobs = Job.objects.filter(id=job_id, user=request.user)
                if len(jobs) == 1:
                    job = jobs[0]
                    job.create_jobinfo_for_task(request.GET.get('task_id'))
                    return HttpResponseRedirect("/job/bigjob/?job_id=%s" % job.id)
                else:
                    return HttpResponseRedirect("/job/bigjob/")
        else:
            job = Job(user=request.user, status="New")
            job.save()
            job.title = "Bigjob-%s" % job.id
            job.save()
            return HttpResponseRedirect("/job/bigjob/?job_id=%s" % job.id)


@login_required
def view_pilot_popup(request, job_id, ur_id):
    if request.method == 'POST':
        form = PilotPopup(request.user, request.POST, request.FILES, job_id=job_id, ur_id=ur_id)
        print form.is_valid(), form.errors
        if form.is_valid():
            form.save(request)
            #messages.success(request, "Job Succesfully created")
        else:
            messages.error(request, "Error in creating job: Inavlid Form")
    else:
        form = PilotPopup(request.user, job_id=job_id, ur_id=ur_id)
    return render_to_response('darewap/bigjob/pilot_popup.html', {'form': form, 'ur_id': ur_id, 'job_id': job_id}, context_instance=RequestContext(request))


@login_required
def view_celery_tasks(request):
    job_id = request.GET.get("jobid")
    task_type = request.GET.get("ttype")
    pilot_id = request.GET.get("pilotid")
    staskid = request.GET.get("staskid")

    if task_type == "start_pilot":
        start_pilot(job_id, pilot_id)

    if task_type == "stop_pilot":
        stop_pilot(job_id, pilot_id)

    if task_type == 'get_pilot_status':
        return HttpResponse(json.dumps(get_pilot_status(job_id, pilot_id)))

    if task_type == 'start_task':
        start_task(staskid)

    if task_type == 'get_task_status':
        return HttpResponse(json.dumps(get_task_status(staskid)))

    return HttpResponse()


@login_required
def view_manage_pilots(request):

    if request.GET.get('del') == 'true':
        pid = request.GET.get('id')
        try:
            ll = UserPilots.objects.get(id=pid)
            ll.delete()
            messages.success(request, "Pilot Succesfully Deleted")
        except:
            messages.success(request, "Pilot Deletion Failed- id=%s" % pid)
        return HttpResponseRedirect("/my-pilots/")

    if request.GET.get('new') == 'true':
        form = UserResourceForm()
        return render_to_response('darewap/pilots/new_pilot.html', {'form': form, 'detail': DEFAULT_PILOT_VALS},  context_instance=RequestContext(request))

    if request.GET.get('edit') == 'true':

        pid = request.GET.get('id')
        try:
            pilot = UserPilots.objects.get(id=pid)
        except:
            pilot = None
        if pilot:
            form = UserPilotsForm(instance=pilot)
            #import pdb;pdb.set_trace()
            try:
                detail = json.dumps(json.loads(pilot.detail))
            except:
                detail = "Json Not supported"

            return render_to_response('darewap/pilots/new_pilot.html', {'form': form, 'pid': pid, 'detail': detail},  context_instance=RequestContext(request))

    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        pid = request.GET.get('id')
        form = None
        if pid:
            try:
                pilot = UserPilots.objects.get(id=pid)
            except:
                pilot = None
            if pilot:
                form = UserPilotsForm(request.POST, request.FILES, instance=pilot)
        if not form:
            form = UserPilotsForm(request.POST, request.FILES)
        if form.is_valid():
            pilot = form.save(request=request)
            messages.success(request, "Pilot Succesfully Saved")
            return render_to_response('darewap/pilots/new_pilot.html', {'form': form, 'pid': pilot.id, 'detail': pilot.detail},  context_instance=RequestContext(request))
        else:
            messages.success(request, "Pilot Saving failed")
            return render_to_response('darewap/pilots/new_pilot.html', {'form': form, 'detail': DEFAULT_PILOT_VALS},  context_instance=RequestContext(request))

    mypilots = UserPilots.objects.filter(user=request.user)
    if mypilots.count() < 1:
        for pilot in DEFAULT_PILOTS.keys():
            up = UserPilots()
            up.user = request.user
            up.name = pilot
            up.detail = json.dumps(DEFAULT_PILOTS[pilot])
            up.save()
    return render_to_response('darewap/pilots/manage_pilots.html', {'mypilots': mypilots}, context_instance=RequestContext(request))


@login_required
def view_all_dare_runs(request):
    runs = DareBigJob.objects.filter(user=request.user)
    return render_to_response('runs/list.html', {'runs': runs}, context_instance=RequestContext(request))


@login_required
def view_dare_run(request, id):
    run = DareBigJob.objects.get(id=id)
    runpilots = DareBigJobPilot.objects.filter(dare_bigjob=run)
    runtasks = DareBigJobTask.objects.filter(dare_bigjob=run)

    form = UserTasksForm()
    send_dict = {
                 'defaultpilots': DefaultDareBigJobPilot.objects.all(),
                 'runpilots': runpilots,
                 'runtasks': runtasks,
                 'run': run,
                 'form': form
                 }

    return render_to_response('runs/view.html', send_dict, context_instance=RequestContext(request))


@login_required
def view_create_run(request):
    if request.method == "POST":
        print request.POST
        if request.POST.get('name'):
            new_run = DareBigJob(user=request.user, status='New', name=request.POST.get('name'))
            new_run.save()
            return HttpResponseRedirect('/runs/%s/' % new_run.id)
    return HttpResponseServerError()


@login_required
def view_run_add_pilot(request, id):
    if request.method == "POST":
        print request.POST
        if request.POST.get('pilot'):
            run = DareBigJob.objects.get(id=id)
            pilot = DefaultDareBigJobPilot.objects.get(id=request.POST.get('pilot'))
            runpilot = DareBigJobPilot()
            for field in DareBigJobPilot._meta.fields:
                if field.name not in ['id', 'defaultdarebigjobpilot_ptr', 'dare_bigjob']:
                    setattr(runpilot, field.name, getattr(pilot, field.name, ''))

            runpilot.user = request.user
            runpilot.number_of_processes = request.POST.get('cores', 8)
            runpilot.walltime = request.POST.get('walltime', 100)
            runpilot.dare_bigjob = run
            runpilot.save()
            return HttpResponseRedirect('/runs/%s/' % run.id)
    return HttpResponseServerError()


@login_required
def view_run_add_task(request, id):
    if request.method == "POST":
        print request.POST
        if request.POST.get('task'):
            run = DareBigJob.objects.get(id=id)
            runtask = DareBigJobTask()
            if request.POST.get('pilot') > -1:
                runtask.dare_bigjob_pilot = DareBigJobPilot.objects.get(request.POST.get('pilot'))
            runtask.name = request.POST.get('name', 'Task')
            runtask.dare_bigjob = run
            runtask.user = request.user
            runtask.save()

            return HttpResponseRedirect('/runs/%s/' % run.id)
    return HttpResponseServerError()
