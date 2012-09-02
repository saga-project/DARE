from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from darewap.models import Job
from .models import Thornfiles
from .forms import ThornfilesForm, CactusJobForm


@login_required
def view_create_job_cactus(request):
    if request.method == 'POST':
        form = ThornfilesForm(request.POST, request.FILES)
        if form.is_valid():
            pass
    else:
        form = CactusJobForm()
    return render_to_response('cactus/create_job.html', {'form': form}, context_instance=RequestContext(request))

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
    documents = Thornfiles.objects.all()

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
    documents = Thornfiles.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'cactus/thornlist.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


