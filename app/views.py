from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import Startup, Mentor, Appointment
from .engine import scheduler, loadzip, sendemails
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime
import numpy
from collections import Counter
import json

@login_required(login_url="/login/")
def index(request):
    return render(request, "summary.html")

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
        try:
            loadzip.loadzip(filename)
        except:
            html_template = loader.get_template('upload_fail.html')
            return HttpResponse(html_template.render(context, request))
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
            k = appointment.keys()
            if 'startup' in k:
                appointmentToUpdate.startupResponse = appointment['startup']
            if 'startupRank' in k:
                appointmentToUpdate.startupRank= appointment['startupRank']
            if 'startupNotes' in k:
                appointmentToUpdate.startupNotes = appointment['startupNotes']
            appointmentToUpdate.save()
    return HttpResponse("ok")


def mentors(request, id):
    mentor = Mentor.objects.get(id=id)
    mentorappointments = Appointment.objects.filter(mentor=mentor, status='pending')
    update_appointments(mentorappointments)
    completedappointments = Appointment.objects.filter(mentor=mentor, status='completed')
    context =  {
        'mentor': mentor,
        'appointments': completedappointments,
    }
    return render(request, "page-blank.html", context=context)


def update_appointments(appointments):
    """
    update the status from pending to completed
    """
    currentdate = date.today()
    currenttime = datetime.today().time()
    for appointment in appointments:
        if appointment.date < currentdate:
            appointment.status = 'completed'
            appointment.save()
        elif appointment.date == currentdate and appointment.endtime <= currenttime:
            appointment.status = 'completed'
            appointment.save()


def startups(request, id):
    startup = Startup.objects.get(id=id)
    startupappointments = Appointment.objects.filter(startup=startup, status='pending')
    update_appointments(startupappointments)
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
            k = appointment.keys()
            if 'mentorresponse' in k:
                appointmentToUpdate.mentorResponse = appointment['mentorresponse']
            if 'mentorRank' in k:
                appointmentToUpdate.mentorRank= appointment['mentorRank']
            if 'mentorNotes' in k:
                appointmentToUpdate.mentorNotes = appointment['mentorNotes']
            appointmentToUpdate.save()
    return HttpResponse("ok")

@login_required(login_url="/login/")
def summary(request):

    if request.method == 'POST':
        scheduler.automaticBooking()
    startups = Startup.objects.all()
    mentors = Mentor.objects.all()
    mylist = []
    finallist = []
    mentordict = {'want': 3, 'willing': 1, 'wont': 0}
    startupdict = {'want': 2, 'willing': 1, 'wont': 0}
    for mentor in mentors:
        mylist2 = [mentor]
        matchlist = []
        for startup in startups:
            try:
                appointment = Appointment.objects.get(startup=startup, mentor=mentor)
                print("ESTE ES EL APPOINTMENT", appointment)
                value = {'id': appointment.id, 'value':mentordict[appointment.mentorResponse] * startupdict[appointment.startupResponse]}
                print("Hay una appointment")
            except:
                value = {'id': 'na','value': "na"}
            mylist2.append(value)
            if value['value'] == "na":
                matchlist.append(-1)
            else:
                matchlist.append(value['value'])
        mylist.append(mylist2)
        finallist.append(matchlist)

    transposed = numpy.transpose(finallist).tolist()
    counters = []
    for element in transposed:
        counters.append(dict(Counter(element)))
    appointments = Appointment.objects.all()
    data = list(zip(startups, counters))
    print(mylist)
    context = {
        'startups': startups,
        'mentors': mentors,
        'mylist': mylist,
        'appointments': appointments,
        'data': data,
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
