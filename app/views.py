from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import Startup, Mentor, Appointment
from .engine import scheduler
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="/login/")
def index(request):
    return render(request, "calendar.html")

@login_required(login_url="/login/")
def pages(request):

    startups_list = Startup.objects.all()
    mentors_list = Mentor.objects.all()
    appointmentlist = Appointment.objects.all()
    context = {
        'startups': startups_list,
        'mentors': mentors_list,
        'appointments': appointmentlist,
    }

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))

@csrf_exempt
def appointmentview(request):
    if request.method == 'POST':
        mentors = Mentor.objects.all()
        scheduler.automaticBooking()
        print("Recibi el post")
        return redirect('/calendar.html')