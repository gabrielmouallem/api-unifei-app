from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.models import Profile
from markers.models import Marker
from schedules.models import Schedule, Classroom
from rest_framework.response import Response

from schedules.serializers import ScheduleSerializer


class RetriveScheduleViewByProfile(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    def get(self, request, *args, **kwargs):
        schedule = Schedule.objects.filter(profile=Profile.objects.get(user_id=self.request.user.id))
        if schedule.exists():
            return Response(data=ScheduleSerializer(instance=schedule.first()).data, status=200)
        else:
            return Response(status=200, data=[])


class AddMarkerToClassroomView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        if self.request.data['classroom_id'] is not None and self.request.data['marker_id']:
            classroom = Classroom.objects.filter(id=self.request.data['classroom_id'])
            if classroom.exists():
                classroom.marker = Marker.objects.get(id=self.request.data['marker_id'])
                classroom.save()
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status=400)