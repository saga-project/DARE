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


def view_static(request, page_type):
    template = 'static/%s.html' % page_type
    return render_to_response(template, {})


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
