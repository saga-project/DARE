from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .models import Thornfiles
from .forms import ThornfilesForm, CactusJobForm
from django.contrib import messages
from .models import Job


@login_required
def view_create_job_cactus(request):
    if request.method == 'POST':
        form = CactusJobForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save(request)
            messages.success(request, "Job Succesfully created")
        else:
            messages.error(request, "Error in creating job: Inavlid Form")
    else:
        form = CactusJobForm(request.user)

    return render_to_response('cactus/create_job.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def view_job_actions(request):
    job_id = request.GET.get('job_id')
    action = (str(request.GET.get('job_id'))).strip()
    if job_id:
        job = Job.objects.filter(id=job_id, user=request.user)[0]
        if action == 'delete':
            job.delete()
            return render_to_response('cactus/job_actions.html', {'message': 'Job %s Deleted' % job_id}, context_instance=RequestContext(request))
        else:
            return render_to_response('cactus/job_actions.html', {'job': job}, context_instance=RequestContext(request))

    else:
        return render_to_response('cactus/job_actions.html', {'message': 'Job not found'}, context_instance=RequestContext(request))


@login_required
def view_thornfileslist(request):
    if request.method == 'POST':
        form = ThornfilesForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Thornfiles(thornfile=request.FILES['docfile'], user=request.user)
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('cactus.views.view_thornfileslist'))
    else:
        form = ThornfilesForm()

    # Load documents for the list page
    documents = Thornfiles.objects.filter(user=request.user)

    # Render list page with the documents and the form
    return render_to_response(
        'cactus/thornlist.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


@login_required
def view_paramfileslist(request):
    if request.method == 'POST':
        form = ThornfilesForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Thornfiles(thornfile=request.FILES['docfile'], user=request.user)
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('cactus.views.view_thornfileslist'))
    else:
        form = ThornfilesForm()

    # Load documents for the list page
    documents = Thornfiles.objects.filter(user=request.user)

    # Render list page with the documents and the form
    return render_to_response(
        'cactus/thornlist.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )



