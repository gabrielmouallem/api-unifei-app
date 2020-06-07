from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from markers.models import GenericMarker, EventMarker, ConstructionMarker, StudyGroupMarker, ExtraActivityMarker
from markers.serializers import GenericMarkerSerializer, EventMarkerSerializer, ConstructionMarkerSerializer, \
    StudyGroupMarkerSerializer, ExtraActivityMarkerSerializer


class ListAllMarkersView(APIView):
    permission_classes = ()
    authentication_classes = (IsAuthenticated, )

    def get(self, request):
        generic_markers = GenericMarker.objects.all()
        event_markers = EventMarker.objects.all()
        construction_markers = ConstructionMarker.objects.all()
        study_group_markers = StudyGroupMarker.objects.all()
        extra_activity_markers = ExtraActivityMarker.objects.all()

        return Response(data={
            "generic_markers": generic_markers,
            "event_markers": event_markers,
            "construction_markers": construction_markers,
            "study_group_markers": study_group_markers,
            "extra_activity_markers": extra_activity_markers,
        })

class GenericMarkerModelView(CreateAPIView):
    permission_classes = ()
    authentication_classes = (IsAuthenticated, )

    serializer_class = GenericMarkerSerializer
    model = GenericMarker

class EventMarkerModelView(CreateAPIView):
    permission_classes = ()
    authentication_classes = (IsAuthenticated, )

    serializer_class = EventMarkerSerializer
    model = EventMarker

class ConstructionMarkerModelView(CreateAPIView):
    permission_classes = ()
    authentication_classes = (IsAuthenticated, )

    serializer_class = ConstructionMarkerSerializer
    model = ConstructionMarker

class StudyGroupMarkerModelView(CreateAPIView):
    permission_classes = ()
    authentication_classes = (IsAuthenticated, )

    serializer_class = StudyGroupMarkerSerializer
    model = StudyGroupMarker

class ExtraActivityMarkerModelView(CreateAPIView):
    permission_classes = ()
    authentication_classes = (IsAuthenticated, )

    serializer_class = ExtraActivityMarkerSerializer
    model = ExtraActivityMarker