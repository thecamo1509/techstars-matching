from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

@shared_task
def send_email_automation():
    msg_html = render_to_string('htmltemplate.html', {})
    msg = EmailMessage(subject="Thank you for mentoring!", body=msg_html, from_email="camilomoralesiml@gmail.com", bcc=['camiloandres.1509@gmail.com', 'oscarnetworkingpro@gmail.com', 'Devbardbudist@hotmail.com', 'danielchinome987@gmail.com', 'joldiazcha@gmail.com'])
    msg.content_subtype = "html"  # Main content is now text/html
    return msg.send()
    print('Un email fue enviado')