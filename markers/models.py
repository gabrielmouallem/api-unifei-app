import requests
from django.db import models
from django.db.models.signals import post_save

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

def on_generic_marker_post_save(sender, instance: GenericMarker, **kwargs):
    try:
        body = {
            'id': instance.id,
            'name': instance.name,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'type': instance.type
        }
        requests.post("http://localhost:80/new-marker", data=body, timeout=5)
    except Exception as ex:
        print(str(ex))

def on_event_marker_post_save(sender, instance: EventMarker, **kwargs):
    try:
        body = {
            'id': instance.id,
            'name': instance.name,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'type': instance.type
        }
        requests.post("http://localhost:80/new-marker", data=body, timeout=5)
    except Exception as ex:
        print(str(ex))

def on_construction_marker_post_save(sender, instance: ConstructionMarker, **kwargs):
    try:
        body = {
            'id': instance.id,
            'name': instance.name,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'type': instance.type
        }
        requests.post("http://localhost:80/new-marker", data=body, timeout=5)
    except Exception as ex:
        print(str(ex))

def on_study_group_marker_post_save(sender, instance: StudyGroupMarker, **kwargs):
    try:
        body = {
            'id': instance.id,
            'name': instance.name,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'type': instance.type
        }
        requests.post("http://localhost:80/new-marker", data=body, timeout=5)
    except Exception as ex:
        print(str(ex))

def on_extra_activity_marker_post_save(sender, instance: ExtraActivityMarker, **kwargs):
    try:
        body = {
            'id': instance.id,
            'name': instance.name,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'type': instance.type
        }
        requests.post("http://localhost:80/new-marker", data=body, timeout=5)
    except Exception as ex:
        print(str(ex))


post_save.connect(on_generic_marker_post_save, sender=GenericMarker)
post_save.connect(on_construction_marker_post_save, sender=ConstructionMarker)
post_save.connect(on_event_marker_post_save, sender=EventMarker)
post_save.connect(on_extra_activity_marker_post_save, sender=ExtraActivityMarker)
post_save.connect(on_study_group_marker_post_save, sender=StudyGroupMarker)