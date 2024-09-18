from django.contrib import admin

from reservations.models import StudentReservation, TeacherSchedule

admin.site.register(TeacherSchedule)
admin.site.register(StudentReservation)
