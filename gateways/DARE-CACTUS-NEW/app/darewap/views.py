from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.shortcuts import render
from .models import Job
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def view_home(request):
    return render(request, 'static/home.html')


def view_about(request):
    return render_to_response('static/about.html', {})


def view_resources(request):
    return render_to_response('static/resources.html', {})


def view_dare_cactus(request):
    return render_to_response('static/dare_cactus.html', {})


def view_contact(request):
    return render_to_response('static/contact.html', {})


def view_software(request):
    return render_to_response('static/software.html', {})


def view_login(request):
    return render_to_response('static/login.html', {})


def view_logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def view_job_list(request):
    jobs = Job.objects.all()
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
