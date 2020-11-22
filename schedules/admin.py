from django.contrib import admin

# Register your models here.
from schedules.models import Schedule, Classroom

admin.site.register(Schedule)
admin.site.register(Classroom)