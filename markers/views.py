import itertools
import json

from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from markers.models import GenericMarker, EventMarker, ConstructionMarker, StudyGroupMarker, ExtraActivityMarker
from markers.serializers import GenericMarkerSerializer, EventMarkerSerializer, ConstructionMarkerSerializer, \
    StudyGroupMarkerSerializer, ExtraActivityMarkerSerializer


class ListAllMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        generic_markers = GenericMarker.objects.all().values()
        event_markers = EventMarker.objects.all().values()
        construction_markers = ConstructionMarker.objects.all().values()
        study_group_markers = StudyGroupMarker.objects.all().values()
        extra_activity_markers = ExtraActivityMarker.objects.all().values()

        return Response(data={
            "data": list(itertools.chain(
                generic_markers,
                event_markers,
                construction_markers,
                study_group_markers,
                extra_activity_markers
        ))}, status=200)


class ListGenericMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        generic_markers = GenericMarker.objects.all()

        return Response(data={
            "generic_markers": generic_markers,
        })


class ListEventMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        event_markers = EventMarker.objects.all()

        return Response(data={
            "event_markers": event_markers,
        })


class ListConstructionMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        construction_markers = ConstructionMarker.objects.all()

        return Response(data={
            "construction_markers": construction_markers,
        })


class ListStudyGroupMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        study_group_markers = StudyGroupMarker.objects.all()

        return Response(data={
            "study_group_markers": study_group_markers,
        })


class ListExtraActivityMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        extra_activity_markers = ExtraActivityMarker.objects.all()

        return Response(data={
            "extra_activity_markers": extra_activity_markers,
        })


class GenericMarkerModelView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = GenericMarkerSerializer
    model = GenericMarker


class EventMarkerModelView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = EventMarkerSerializer
    model = EventMarker


class ConstructionMarkerModelView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = ConstructionMarkerSerializer
    model = ConstructionMarker


class StudyGroupMarkerModelView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = StudyGroupMarkerSerializer
    model = StudyGroupMarker


class ExtraActivityMarkerModelView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = ExtraActivityMarkerSerializer
    model = ExtraActivityMarker
