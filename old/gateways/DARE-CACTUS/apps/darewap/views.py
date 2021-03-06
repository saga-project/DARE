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
from .models import Job, UserContext, UserResource
from .forms import UserContextTable, UserContextForm, UserResourceTable, UserResourceForm


def view_home(request):
    return render(request, 'static/home.html')


def view_static(request, page_type):
    template = 'static/%s.html' % page_type
    return render(request, template)


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
