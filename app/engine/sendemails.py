from ..models import Appointment
from datetime import date
from ..tasks import send_email_automation

def sendemails():
    appointments = Appointment.objects.filter(date=date.today(),)
    objectslist = []
    """for appointment in appointments:
        if appointment.mentor.timeSlot == 'AM':
            myobject = {'id': appointment.mentor.id, 'email': appointment.mentor.email}
            if myobject not in objectslist:
                objectslist.append(myobject)"""
    """objectslist.append({'id': 1, 'email': 'ing.heimer.rojas@gmail.com'})"""
    objectslist.append({'id': 2, 'email': 'camiloandres.1509@gmail.com'})
    
    """for objects in objectslist:
        send_email_automation(objects['email'], objects['id'])"""
    return objectslist
