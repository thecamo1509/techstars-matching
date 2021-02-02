from ..models import Appointment
from datetime import date

def sendemails():
    appointments = Appointment.objects.filter(date=date.today())
    print(appointments)
    return None