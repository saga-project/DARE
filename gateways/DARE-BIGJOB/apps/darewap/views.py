from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.template import RequestContext
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Job, UserContext, UserResource, UserTasks
from .forms import UserContextTable, UserContextForm, UserResourceTable, UserResourceForm, UserTasksForm
from .forms import PilotForm, ResourceEditConf, BigJobForm
from .tasks import start_pilot


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
    jobs = Job.objects.filter(user=request.user)
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
        return render_to_response('darewap/new_task_script.html', {'form': form},  context_instance=RequestContext(request))

    if request.GET.get('edit') == 'true':
        tid = request.GET.get('id')
        try:
            task = UserTasks.objects.get(id=tid)
        except:
            task = None
        if task:
            form = UserTasksForm(instance=task)
            return render_to_response('darewap/new_task_script.html', {'form': form, 'tid': tid},  context_instance=RequestContext(request))

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
            return render_to_response('darewap/new_task_script.html', {'form': form, 'tid': task.id},  context_instance=RequestContext(request))
        else:
            return render_to_response('darewap/new_task_script.html', {'form': form},  context_instance=RequestContext(request))

    mytasks = UserTasks.objects.filter(user=request.user)
    return render_to_response('darewap/manage_tasks.html', {'mytasks': mytasks}, context_instance=RequestContext(request))


@login_required
def view_bigjob(request):
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
        job = Job(user=request.user, status="New")
        job.save()
        job.title = "Bigjob-%s" % job.id
        job.save()
        bigjobform = BigJobForm(request.user)
        pilotform = PilotForm(request.user)
        mytasks = UserTasks.objects.filter(user=request.user)

        retrun_dict = {'bigjobform': bigjobform, "pilotform": pilotform, 'job_id': job.id, "mytasks": mytasks}

    return render_to_response('darewap/bigjob/main.html', retrun_dict, context_instance=RequestContext(request))


@login_required
def view_pilot_popup(request, job_id, pilot):
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
    return render_to_response('darewap/bigjob/pilot_popup.html', {'form': form, 'pilot': pilot, 'job_id': job_id}, context_instance=RequestContext(request))

