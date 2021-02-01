from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .models import Appointment, Mentor
from datetime import date


def send_email_automation(email, id):
    appointments = Appointment.objects.filter(date=date.today())
    msg_html = render_to_string('htmltemplate.html', {'mentorid': id})
    msg = EmailMessage(subject="Thank you for mentoring!", body=msg_html, from_email="alba.montana@techstarsassociates.com", bcc=[email])
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
    print('Un email fue enviado')

    todayappointments = Appointment.objects.filter(date=date.today())
    emaillist = ['camiloandres.1509@gmail.com', 'ing.heimer.rojas@gmail.com']
    idlist = ['4', '7']
    """for appointment in todayappointments:
        emaillist.append(appointment.mentor.email)
        idlist.append(appointment.mentor.id)"""

    bcc = set(emaillist)
    mentorids = set(idlist)

@shared_task
def send_massive_emails(bcc, mentorids):
    for i in zip(bcc, mentorids):
        send_email_automation(*i)   