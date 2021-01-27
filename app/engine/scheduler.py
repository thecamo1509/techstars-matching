import json
from ..models import Appointment, Startup, Mentor
from datetime import date, datetime, timedelta


TIME_BlOCKS = {
    'am': [
        (8, 00),
        (8, 20),
        (8, 40),
        (9, 00),
        (9, 20),
        (9, 40),
        (10, 00),
        (10, 20),
        (10, 40),
        (11, 00),
        (11, 20),
        (11, 40),
        (12, 00),
    ],
    'pm': [
        (14, 00),
        (14, 20),
        (14, 40),
        (15, 00),
        (15, 20),
        (15, 40),
        (16, 00),
        (16, 20),
        (16, 40),
        (17, 00),
        (17, 20),
        (17, 40),
        (18, 00),
    ]
}

WEEKDAYS = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday'}

mymentors = Mentor.objects.all()
currentday = date.today()

next_monday = currentday + timedelta((-currentday.weekday()) % 7) if currentday + timedelta((-currentday.weekday()) % 7) != currentday else currentday + timedelta(((-currentday.weekday()) % 7) + 7)
next_tuesday = currentday + timedelta((1-currentday.weekday()) % 7) if currentday + timedelta((1-currentday.weekday()) % 7) != currentday else currentday + timedelta(((1-currentday.weekday()) % 7) + 7)
next_wednesday = currentday + timedelta((2-currentday.weekday()) % 7) if currentday + timedelta((2-currentday.weekday()) % 7) != currentday else currentday + timedelta(((2-currentday.weekday()) % 7) + 7)
next_thursday = currentday + timedelta((3-currentday.weekday()) % 7) if currentday + timedelta((3-currentday.weekday()) % 7) != currentday else currentday + timedelta(((3-currentday.weekday()) % 7) + 7)
next_friday = currentday + timedelta((4-currentday.weekday()) % 7) if currentday + timedelta((4-currentday.weekday()) % 7) != currentday else currentday + timedelta(((4-currentday.weekday()) % 7) + 1)

NEXT_DATES = {
    0: next_monday,
    1: next_tuesday,
    2: next_wednesday,
    3: next_thursday,
    4: next_friday,
}

def automaticBooking():
    for daycode, day in WEEKDAYS.items():
        mentorslistmorning = Mentor.objects.filter(day=day, timeSlot='AM')
        mentorslistafternoon = Mentor.objects.filter(day=day, timeSlot='PM')
        if mentorslistmorning.count() != 0:
            automatedSchedulerMorning(mentorslistmorning, NEXT_DATES[daycode])
        else:
            pass
        if mentorslistafternoon.count() != 0:
            automatedSchedulerAfternoon(mentorslistafternoon, NEXT_DATES[daycode])
        else:
            pass


def automatedSchedulerMorning(mentors, date):
    for mentor in mentors:
        startups = Startup.objects.filter(mentor=mentor)
        for startup in startups:
            mytimeslot = TIME_BlOCKS['am'].copy()
            for timeslot in mytimeslot: 
                currentdate = date
                currenttime = datetime.today().time()
                newtime = currenttime.replace(timeslot[0],timeslot[1], 00, 000000)
                appointmentsmentor = Appointment.objects.filter(mentor=mentor, date=currentdate, time=newtime)
                if appointmentsmentor.count() == 0:
                    appointmentsstartup = Appointment.objects.filter(startup=startup, date=currentdate, time=newtime)
                    if appointmentsstartup.count() == 0:
                        appointmentfilter = Appointment.objects.filter(mentor=mentor, startup=startup, date=currentdate)
                        if appointmentfilter.count() == 0:
                            newappointment = Appointment(mentor=mentor, startup=startup, date=currentdate, time=newtime, meet="https://meet.google.com/iki-zduu-fnj", status="Pending")
                            newappointment.save()
                            mytimeslot.remove(timeslot)
                            break

def automatedSchedulerAfternoon(mentors, date):
    for mentor in mentors:
        startups = Startup.objects.filter(mentor=mentor)
        for startup in startups:
            mytimeslot = TIME_BlOCKS['pm'].copy()
            for timeslot in mytimeslot: 
                currentdate = date
                currenttime = datetime.today().time()
                newtime = currenttime.replace(timeslot[0],timeslot[1], 00, 000000)
                appointmentsmentor = Appointment.objects.filter(mentor=mentor, date=currentdate, time=newtime)
                if appointmentsmentor.count() == 0:
                    appointmentsstartup = Appointment.objects.filter(startup=startup, date=currentdate, time=newtime)
                    if appointmentsstartup.count() == 0:
                        appointmentfilter = Appointment.objects.filter(mentor=mentor, startup=startup, date=currentdate)
                        if appointmentfilter.count() == 0:
                            newappointment = Appointment(mentor=mentor, startup=startup, date=currentdate, time=newtime, meet="https://meet.google.com/iki-zduu-fnj", status="Pending")
                            newappointment.save()
                            mytimeslot.remove(timeslot)
                            break

