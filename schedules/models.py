from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

# Create your models here.
from authentication.models import Profile
from markers.models import Marker


class Classroom(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    marker = models.OneToOneField(Marker, null=True, blank=True, on_delete=models.SET_NULL)
    content = JSONField(default=list)


class Schedule(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    classrooms = models.ManyToManyField(Classroom)

    def __str__(self):
        return "Horário de ID: " + str(self.id) + " | " + str(self.profile.name)