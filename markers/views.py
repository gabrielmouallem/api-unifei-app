import itertools
import json

from django.http import Http404
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Profile
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

        generic_marker = GenericMarker.objects.filter(pk=self.kwargs.get('pk'), type=3).first()
        if generic_marker is not None:
            return Response(data={
                "data": GenericMarkerSerializer(instance=generic_marker).data,
            }, status=200)

        study_group_marker = StudyGroupMarker.objects.filter(pk=self.kwargs.get('pk')).first()
        if study_group_marker is not None:
            return Response(data={
                "data": StudyGroupMarkerSerializer(instance=study_group_marker).data,
            }, status=200)

        construction_marker = ConstructionMarker.objects.filter(pk=self.kwargs.get('pk')).first()
        if construction_marker is not None:
            return Response(data={
                "data": ConstructionMarkerSerializer(instance=construction_marker).data,
            }, status=200)

        event_marker = EventMarker.objects.filter(pk=self.kwargs.get('pk')).first()
        if event_marker is not None:
            return Response(data={
                "data": EventMarkerSerializer(instance=event_marker).data,
            }, status=200)

        extra_activity_marker = ExtraActivityMarker.objects.filter(pk=self.kwargs.get('pk')).first()
        if extra_activity_marker is not None:
            return Response(data={
                "data": ExtraActivityMarkerSerializer(instance=extra_activity_marker).data,
            }, status=200)

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

    def post(self, request, *args, **kwargs):
        temp_request = request
        temp_request.data['profile'] = Profile.objects.filter(user_id=self.request.user.id).first().id
        return self.create(temp_request, *args, **kwargs)



class EventMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = EventMarkerSerializer
    model = EventMarker

    def post(self, request, *args, **kwargs):
        temp_request = request
        temp_request.data['profile'] = Profile.objects.filter(user_id=self.request.user.id).first().id
        return self.create(temp_request, *args, **kwargs)

class ConstructionMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = ConstructionMarkerSerializer
    model = ConstructionMarker

    def post(self, request, *args, **kwargs):
        temp_request = request
        temp_request.data['profile'] = Profile.objects.filter(user_id=self.request.user.id).first().id
        return self.create(temp_request, *args, **kwargs)

class StudyGroupMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = StudyGroupMarkerSerializer
    model = StudyGroupMarker

    def post(self, request, *args, **kwargs):
        temp_request = request
        temp_request.data['profile'] = Profile.objects.filter(user_id=self.request.user.id).first().id
        return self.create(temp_request, *args, **kwargs)

class ExtraActivityMarkerCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    serializer_class = ExtraActivityMarkerSerializer
    model = ExtraActivityMarker

    def post(self, request, *args, **kwargs):
        temp_request = request
        temp_request.data['profile'] = Profile.objects.filter(user_id=self.request.user.id).first().id
        return self.create(temp_request, *args, **kwargs)

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
