import itertools
import json

from django.http import Http404
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from markers.models import GenericMarker, EventMarker, ConstructionMarker, StudyGroupMarker, ExtraActivityMarker, Marker
from markers.serializers import GenericMarkerSerializer, EventMarkerSerializer, ConstructionMarkerSerializer, \
    StudyGroupMarkerSerializer, ExtraActivityMarkerSerializer, MarkerSerializer


class ListAllMarkersView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):
        extra_activity_markers = ExtraActivityMarker.objects.all().order_by('id').values()
        study_group_markers = StudyGroupMarker.objects.all().order_by('id').values()
        event_markers = EventMarker.objects.all().order_by('id').values()
        construction_markers = ConstructionMarker.objects.all().order_by('id').values()
        generic_markers = GenericMarker.objects.all().order_by('id').filter(type=3).values()

        return Response(data={
            "data": list(itertools.chain(
                study_group_markers,
                extra_activity_markers,
                event_markers,
                generic_markers,
                construction_markers,
        ))}, status=200)


class SelectedMarkerView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request, *args, **kwargs):

        try:
            generic_marker = GenericMarker.objects.filter(pk=self.kwargs.get('pk'), type=3).values()
            if generic_marker.count() == 1:
                return Response(data={
                    "data": generic_marker[0],
                }, status=200)
        except:
            pass

        try:
            study_group_marker = StudyGroupMarker.objects.filter(pk=self.kwargs.get('pk')).values()
            if study_group_marker.count() == 1:
                return Response(data={
                    "data": study_group_marker[0],
                }, status=200)
        except:
            pass

        try:
            construction_marker = ConstructionMarker.objects.filter(pk=self.kwargs.get('pk')).values()
            if construction_marker.count() == 1:
                return Response(data={
                    "data": construction_marker[0],
                }, status=200)
        except:
            pass

        try:
            event_marker = EventMarker.objects.filter(pk=self.kwargs.get('pk')).values()
            if event_marker.count() == 1:
                return Response(data={
                    "data": event_marker[0],
                }, status=200)
        except:
            pass

        try:
            extra_activity_marker = ExtraActivityMarker.objects.filter(pk=self.kwargs.get('pk')).values()
            if extra_activity_marker.count() == 1:
                return Response(data={
                    "data": extra_activity_marker[0],
                }, status=200)
        except:
            pass

        return Response(status=404)


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


class GenericMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = GenericMarkerSerializer
    model = GenericMarker


class EventMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = EventMarkerSerializer
    model = EventMarker


class ConstructionMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = ConstructionMarkerSerializer
    model = ConstructionMarker


class StudyGroupMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = StudyGroupMarkerSerializer
    model = StudyGroupMarker


class ExtraActivityMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = ExtraActivityMarkerSerializer
    model = ExtraActivityMarker


class MarkerDestroyView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    queryset = Marker.objects.all()
    serializer_class = MarkerSerializer
    lookup_field = 'pk'


class GenericMarkerUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = GenericMarker.objects.all()
    serializer_class = GenericMarkerSerializer
    lookup_field = 'pk'


class EventMarkerUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    queryset = EventMarker.objects.all()
    serializer_class = EventMarkerSerializer
    lookup_field = 'pk'


class ConstructionMarkerUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    queryset = ConstructionMarker.objects.all()
    serializer_class = ConstructionMarkerSerializer
    lookup_field = 'pk'

class StudyGroupMarkerUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    queryset = StudyGroupMarker.objects.all()
    serializer_class = StudyGroupMarkerSerializer
    lookup_field = 'pk'


class ExtraActivityMarkerUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    queryset = ExtraActivityMarker.objects.all()
    serializer_class = ExtraActivityMarkerSerializer
    lookup_field = 'pk'
