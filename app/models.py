from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
TIME_SLOTS_CHOICES = [
    ('AM', 'Morning'),
    ('PM', 'Afternoon'),
    ('undefined', 'Undefined'),
]

DAY_CHOICES = [
    ('monday', 'Monday'),
    ('tuesday', 'Tuesday'),
    ('wednesday', 'Wednesday'),
    ('thursday', 'Thursday'),
    ('friday', 'Friday'),
    ('undefined', 'Undefined'),
]

RESPONSES = [
    ('want', 'Want'),
    ('wont', 'Wont'),
    ('willing', 'Willing'),
]

STATUSES = [
    ('pending', 'Pending'),
    ('in progress', 'In Progress'),
    ('completed', 'Completed'),
]


class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'startup'),
      (2, 'mentor'),
      (3, 'staff'),
  )
    profile_pic = models.ImageField()
    user_type = models.PositiveSmallIntegerField(default= 3, choices=USER_TYPE_CHOICES, null=True)

class Startup(models.Model):
    companyName = models.CharField(max_length=200)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    whatwedo = models.CharField(max_length=400)
    startupPic = models.URLField()

    def __str__(self):
        return self.companyName


class Mentor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True)
    day = models.CharField(max_length=200, choices=DAY_CHOICES)
    timeSlot = models.CharField(max_length=50, choices=TIME_SLOTS_CHOICES)
    startup = models.ManyToManyField(Startup)
    mentorPic = models.URLField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    endtime = models.TimeField()
    status = models.CharField(max_length=50, choices=STATUSES)
    mentorResponse = models.CharField(max_length=200, choices=RESPONSES, blank=True)
    startupResponse = models.CharField(max_length=200, choices=RESPONSES, blank=True)
    mentorNotes = models.CharField(max_length=10000, blank=True)
    startupNotes = models.CharField(max_length=10000, blank=True)
    mentorRank = models.IntegerField(blank=True, null=True)  # mentor response
    startupRank = models.IntegerField(blank=True, null=True)  # startup response

class LeadMentor(models.Model):
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    startup = models.OneToOneField(Startup, on_delete=models.CASCADE)

class AdHocMentor(models.Model):
    mentor = models.OneToOneField(Mentor, on_delete=models.CASCADE)
    startups = models.ManyToManyField(Startup)
