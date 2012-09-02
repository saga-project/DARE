from django.shortcuts import render_to_response


def view_home(request):
    return render_to_response('static/home.html', {})


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
