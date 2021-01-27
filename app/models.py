from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TIME_SLOTS_CHOICES = [
    ('AM', 'Morning'),
    ('PM', 'Afternoon')
]

DAY_CHOICES = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
]

class Startup(models.Model):
    companyName = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.companyName
    

class Mentor(models.Model):
    name = models.CharField(max_length=200)
    day = models.CharField(max_length=200, choices=DAY_CHOICES)
    timeSlot = models.CharField(max_length=50, choices=TIME_SLOTS_CHOICES)
    startup = models.ManyToManyField(Startup)
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    meet = models.URLField()
    status = models.CharField(max_length=50)
