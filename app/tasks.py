from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from .models import Appointment, Mentor
from datetime import date

def send_email_automation(email, id):
    appointments = Appointment.objects.filter(date=date.today())
    mentor = Mentor.objects.get(id=id)
    mentorname = mentor.name
    message = """
    Hi {}

    Thank you for sharing your time with the companies today. When you get a chance, please select the companies you want to mentor, will not mentor, or are willing to mentor via this very short form https://techstars-matchmaking.herokuapp.com/mentors/{}
    
    With appreciation,
    Malte, Alba and Andres
    """.format(mentorname, id)
    msg = EmailMessage(subject="[Action Required] Which companies do you want to mentor?", body=message, from_email="alba.montana@techstarsassociates.com", bcc=[email])
    return msg.send()


@shared_task
def send_massive_emails(bcc, mentorids):
    for i in zip(bcc, mentorids):
        send_email_automation(*i)   