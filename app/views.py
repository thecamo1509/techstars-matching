from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import Startup, Mentor, Appointment
from .engine import scheduler, loadzip
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime
import json

@login_required(login_url="/login/")
def index(request):
    return render(request, "calendar.html")

@login_required(login_url="/login/")
def pages(request):
    checkresults = False
    startups_list = Startup.objects.all()
    mentors_list = Mentor.objects.all()
    appointmentlist = Appointment.objects.all()
    currentstartup = Startup.objects.get(user=request.user)
    mymentors = Mentor.objects.filter(startup=currentstartup)
    todayappointments = Appointment.objects.filter(startup=currentstartup, date=str(date.today()))
    completedappointments = Appointment.objects.filter(status="completed", startup=currentstartup)
    if completedappointments.count() != 0:
        checkresults = True
    currenttime = datetime.now().time()
    context = {
        'startups': startups_list,
        'mentors': mentors_list,
        'appointments': appointmentlist,
        'currentstartup': currentstartup,
        'mymentors': mymentors,
        'todayappointments': todayappointments,
        'currenttime': currenttime,
        'checkresults': checkresults,
        "completedappointments": completedappointments,
        "range": range(7, completedappointments.count() + 1)
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
        uploaded_file_url = fs.url(filename)
        print("Recibi el post")
        loadzip.loadzip(filename)
        """except:
            html_template = loader.get_template('upload_fail.html')
            return HttpResponse(html_template.render(context, request))"""
        html_template = loader.get_template('upload2.html')
        return HttpResponse(html_template.render(context, request))
    html_template = loader.get_template('upload.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
def updateappointmentstartup(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        for appointment in body:
            print(appointment)
            appointmentToUpdate = Appointment.objects.get(id=appointment['id'])
            appointmentToUpdate.startupResponse = appointment['startup']
            appointmentToUpdate.status = "completed"
            appointmentToUpdate.save()
    return HttpResponse("ok")


def mentors(request, id):
    mentor = Mentor.objects.get(id=id)
    mentorappointments = Appointment.objects.filter(mentor=mentor, status='completed')
    context =  {
        'mentor': mentor,
        'appointments': mentorappointments,
    }
    return render(request, "page-blank.html", context=context)

def startups(request, id):
    startup = Startup.objects.get(id=id)
    currentdate = date.today()
    currenttime = datetime.today().time()
    startupappointments = Appointment.objects.filter(startup=startup, status='pending')
    for appointment in startupappointments:
        print("La hora es: {}".format(currenttime))
        if appointment.date <= currentdate:
            if appointment.endtime <= currenttime:
                print("I changed the status")
                appointment.status = 'completed'
                appointment.save()
            else:
                pass
        else:
            pass
    completedappointments = Appointment.objects.filter(startup=startup, status='completed')
    context =  {
        'startup': startup,
        'appointments': completedappointments,
    }
    return render(request, "userview.html", context=context)

@csrf_exempt
def updateappointmentmentor(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        for appointment in body:
            appointmentToUpdate = Appointment.objects.get(id=appointment['id'])
            appointmentToUpdate.mentorResponse = appointment['mentorresponse']
            appointmentToUpdate.save()
    return HttpResponse("ok")

@login_required(login_url="/login/")
def summary(request):
    startups = Startup.objects.all()
    mentors = Mentor.objects.all()
    mylist = []
    mentordict = {'want': 3, 'willing': 1, 'wont': 0}
    startupdict = {'want': 2, 'willing': 1, 'wont': 0}
    for mentor in mentors:
        mylist2 = [mentor]
        for startup in startups:
            try:
                appointment = Appointment.objects.get(startup=startup, mentor=mentor)
                value = {'id': appointment.id, 'value':mentordict[appointment.mentorResponse] * startupdict[appointment.startupResponse]}
            except:
                value = {'id': 'na','value': "na"}
            mylist2.append(value)
        mylist.append(mylist2)

    appointments = Appointment.objects.all()
    context = {
        'startups': startups,
        'mentors': mentors,
        'mylist': mylist,
        'appointments': appointments,
    }
    return render(request, "summary.html", context=context)


def results(request, appointmentid):
    mentor = Mentor.objects.get(id=id)
    mentorappointments = Appointment.objects.filter(mentor=mentor, status='completed')
    context =  {
        'mentor': mentor,
        'appointments': mentorappointments,
    }
    return render(request, "results.html", context=context)