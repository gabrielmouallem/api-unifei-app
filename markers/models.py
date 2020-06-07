from django.db import models

from markers.constants import MARKER_TYPES, EVENT_TYPES, CONSTRUCTION_TYPES


class GenericMarker(models.Model):

    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.IntegerField(choices=MARKER_TYPES, default=0)

    description = models.CharField(max_length=300, default='')

    latitude = models.CharField(max_length=100, default='')
    longitude = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ('type',)


class EventMarker(GenericMarker):

    event_type = models.IntegerField(choices=EVENT_TYPES, null=False, blank=False)
    event_date = models.DateTimeField()

    class Meta:
        ordering = ('event_type',)


class ConstructionMarker(GenericMarker):

    construction_type = models.IntegerField(choices=CONSTRUCTION_TYPES, null=False, blank=False)

    class Meta:
        ordering = ('construction_type',)


class StudyGroupMarker(GenericMarker):

    group_size = models.PositiveIntegerField(null=False, blank=False)
    discipline = models.CharField(max_length=300, default='')
    class_group = models.CharField(max_length=300, default='')

    class Meta:
        ordering = ('group_size',)


class ExtraActivityMarker(GenericMarker):

    activity_type = models.CharField(max_length=300, default='')

    class Meta:
        ordering = ('activity_type',)