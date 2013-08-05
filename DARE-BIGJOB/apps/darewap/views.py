from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from .models import DareBigJob, DareBigJobTask, DareBigJobPilot, DefaultDareBigJobPilot
from .forms import UserTasksForm
from .tasks import start_run_pilot, stop_run_pilot, start_run_task, stop_run_task
import datetime
from . import tasks

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
def view_all_dare_runs(request):
    runs = DareBigJob.objects.filter(user=request.user)
    return render_to_response('runs/list.html', {'runs': runs}, context_instance=RequestContext(request))


@login_required
def view_dare_run(request, id):
    if request.GET.get('created'):
        messages.success(request, "You have successfully created a Job! Please go ahead and allocate Pilots and add Tasks")

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
        if request.POST.get('name'):
            new_run = DareBigJob(user=request.user, status='New', name=request.POST.get('name'))
            new_run.save()
            return HttpResponseRedirect('/runs/%s/?created=true' % new_run.id)
    return HttpResponseServerError()


@login_required
def view_run_add_pilot(request, id):
    if request.method == "POST":
        if request.POST.get('pilot'):
            run = DareBigJob.objects.get(id=id)
            pilot = DefaultDareBigJobPilot.objects.get(id=request.POST.get('pilot'))
            runpilot = DareBigJobPilot()
            runpilot.user = request.user
            runpilot.dare_bigjob = run
            runpilot.time_started = datetime.datetime.now()

            for field in ['name', 'status', 'pilot_type', 'service_url', 'data_service_url', 'working_directory',
                        'cores_per_node', 'number_of_processes', 'queue', 'project', 'walltime']:
                    setattr(runpilot, field, getattr(pilot, field, ''))

            runpilot.number_of_processes = request.POST.get('cores', 8)
            runpilot.walltime = request.POST.get('walltime', 100)
            runpilot.save()
            return HttpResponseRedirect('/runs/%s/' % run.id)
    return HttpResponseServerError()


@login_required
def view_run_add_task(request, id):
    if request.method == "POST" and request.POST.get('script') and len(request.POST.get('script')) > 0:
        run = DareBigJob.objects.get(id=id)
        runtask = DareBigJobTask()
        if request.POST.get('pilot') > -1:
            runtask.dare_bigjob_pilot = DareBigJobPilot.objects.get(id=request.POST.get('pilot'))
        runtask.name = request.POST.get('name', 'Task')
        runtask.dare_bigjob = run
        runtask.user = request.user
        runtask.script = request.POST.get('script')
        runtask.save()
        return HttpResponseRedirect('/runs/%s/' % run.id)
    return HttpResponseServerError()


@login_required
def view_run_pilot_celery_action(request, id):
    ctask_type = request.GET.get("type")
    pilot_id = request.GET.get("pilot_id")
    if ctask_type == "start":
        start_run_pilot(pilot_id)

    if ctask_type == "stop":
        stop_run_pilot(pilot_id)

    if ctask_type == "update":
        tasks.update_status_run_pilot(pilot_id)

    return HttpResponseRedirect('/runs/%s/' % id)


@login_required
def view_run_task_celery_action(request, id):
    ctask_type = request.GET.get("type")
    task_id = request.GET.get("task_id")
    if ctask_type == "start":
        start_run_task(task_id)

    if ctask_type == "stop":
        stop_run_task(task_id)
    if ctask_type == "update":
        tasks.update_status_run_task(task_id)

    return HttpResponseRedirect('/runs/%s/' % id)
