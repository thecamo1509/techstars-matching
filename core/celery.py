import os
from ..app.models import Appointment
from datetime import date

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

emaillist = ['malte.witt@techstars.com', 'camiloandres.1509@gmail.com']
apointments = Appointment.objects.filter(date=date.today())
for appointment in appointments:
    print(appointment)


app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'app.tasks.send_massive_emails',
        'schedule': 30,
        'args': [emaillist, idlist]
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')