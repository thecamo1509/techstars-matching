from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import Startup, Mentor, Appointment
from .engine import scheduler, loadmentors
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime

CHECKRESULTS = True

@login_required(login_url="/login/")
def index(request):
    return render(request, "calendar.html")

@login_required(login_url="/login/")
def pages(request):

    startups_list = Startup.objects.all()
    mentors_list = Mentor.objects.all()
    appointmentlist = Appointment.objects.all()
    currentstartup = Startup.objects.get(user=request.user)
    mymentors = Mentor.objects.filter(startup=currentstartup)
    todayappointments = Appointment.objects.filter(startup=currentstartup, date=str(date.today()))
    completedappointments = Appointment.objects.filter(status="completed", startup=currentstartup)
    currenttime = datetime.now().time()
    context = {
        'startups': startups_list,
        'mentors': mentors_list,
        'appointments': appointmentlist,
        'currentstartup': currentstartup,
        'mymentors': mymentors,
        'todayappointments': todayappointments,
        'currenttime': currenttime,
        'checkresults': CHECKRESULTS,
        "completedappointments": completedappointments,
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

def uploadfile(request):
    startups_list = Startup.objects.all()
    mentors_list = Mentor.objects.all()
    appointmentlist = Appointment.objects.all()
    context = {
        'startups': startups_list,
        'mentors': mentors_list,
        'appointments': appointmentlist,
    }
    if request.method == 'POST' and request.FILES.get('file', False):
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        mentors = Mentor.objects.all()
        scheduler.automaticBooking()
        uploaded_file_url = fs.url(filename)
        print("Recibi el post")
        loadmentors.loaddata(filename)

        html_template = loader.get_template('upload2.html')
        return HttpResponse(html_template.render(context, request))
    html_template = loader.get_template('upload.html')
    return HttpResponse(html_template.render(context, request))
