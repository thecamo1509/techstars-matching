from ..models import Appointment
from datetime import date

appointments = Appointment.objects.filter(date=date.today())
print(appointments)