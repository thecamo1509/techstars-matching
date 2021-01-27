from django.contrib import admin
from .models import Appointment, Startup, Mentor

# Register your models here.
admin.site.register(Startup)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('startup','mentor', 'date', 'time', 'status')
    search_fields = ('startup', 'mentor',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Appointment, AppointmentAdmin)

class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'timeSlot')
    search_fields = ('name', 'day')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Mentor, MentorAdmin)