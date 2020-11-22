import json

from django.conf import settings
from django.contrib.auth.models import User, UserManager
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from authentication.models import Profile
from authentication.serializers import UserSerializer, ProfileSerializer
from django.forms.models import model_to_dict
import base64, os
import pdfplumber

from schedules.models import Schedule, Classroom
from schedules.serializers import ScheduleSerializer


def extract_signatures(pdfpath, profile):

    def remove_spaces(string):
        return "".join(string.rstrip().lstrip())
    try:
        # signatures = []
        with pdfplumber.open(pdfpath) as pdf:
            table1 = pdf.pages[0].extract_tables()[0][1:]
        schedule = Schedule.objects.create(profile=profile)
        for val in table1:
            if 'Local:' in val[1] and 'Tipo:' in val[1] and 'MATRICULADO' in val[3]:

                code = remove_spaces(val[0]).upper()
                group = remove_spaces(val[2]).title()
                schedules = val[4].split()
                about = val[1].split('\n')
                # Tipo: DISCIPLINA Local: sala de aula virtual
                classroom_type = about[-1].split('Local:')
                classroom = remove_spaces(classroom_type[-1]).title()
                stype = remove_spaces(classroom_type[0].split('Tipo:')[-1]).title()
                professor = remove_spaces(about[-2]).title()
                name = remove_spaces((' '.join(about[0:-2]))).title()
                classroom = Classroom.objects.create(profile=profile, content={"name": name, "code": code, "type": stype, "professor": professor, "classroom": classroom, "group": group, "schedules": schedules})
                schedule.classrooms.add(classroom)
                # signatures.append({"name": name, "code": code, "type": stype, "professor": professor, "classroom": classroom, "group": group, "schedules": schedules})
        return ScheduleSerializer(instance=schedule).data
    except Exception as ex:
        print("Signature exception ", str(ex))
        return -1

class SendPdfView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post (self, request):
        try:
            profile = Profile.objects.get(user_id=self.request.user.pk)
            data = request.data['data']
            with open(os.path.expanduser('./myschedule.pdf'), 'wb') as fout:
                fout.write(base64.b64decode(data))

            # Caminho do arquivo
            path = './myschedule.pdf'
            # passar o path na função do juninho

            object_data = extract_signatures(path, profile)
            print(object_data)
            if object_data != -1:
                # Expected json string
                # data = json.dumps([ob.__dict__ for ob in object_data], sort_keys=True, indent=4, ensure_ascii=False)
                return Response(data={"data": object_data})
            else:
                return Response(data={"data": None, "error": 'error on signature function.'})

        except Exception as ex:
            return Response(data={"data": None, "error": str(ex)})

class LoginView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = json.loads(request.body)

        if not body.get('method'):
            return Response(status=400)

        if body['method'] == 'google':

            try:
                googleUser = id_token.verify_oauth2_token(
                    body['id_token'], requests.Request(), settings.GOOGLE_CLIENT_ID)
            except Exception as ex:
                return Response(str(ex), status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

            if googleUser['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return Response(data={"Google internal problem."}, status=400)

            try:
                user = User.objects.get(email=googleUser['email'])

            except Exception as ex:
                if body.get('email'):
                    username = body['email']
                    password = User.objects.make_random_password()
                    user = User.objects.create_user(username, username)
                    user.set_password(password)
                    token, _ = Token.objects.get_or_create(user=user)
                    print("google - created account for ", username)
                    return Response({'token': token.key}, status=200)

                else:
                    return Response(data={"Error creating google account."}, status=400)

            print("google - logged on ", body['email'])
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)


        if (body['method'] == 'password'):

            if body.get('email'):
                try:
                    username = User.objects.get(email=body['email']).username
                except User.DoesNotExist:
                    return Response(data={"Email not registered."}, status=400)

            elif body.get('username'):
                username = body['username']

            else:
                return Response(data={"Username not registered."}, status=400)

            if not body.get('password'):
                return Response(data={"Missing or invalid password."}, status=400)

            user = authenticate(username=username, password=body['password'])

            if user is None:
                return Response(data={"Username or password invalid."}, status=400)

            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=200)

        else:
            return Response(data={"Missing authentication method."}, status=400)


class CreateUserView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = json.loads(request.body)
        serializer_user = UserSerializer(data=request.data)

        username = body['username']
        email = body['email']
        password = body['password']

        if serializer_user.is_valid():  # Cria o User
            user = User.objects.create_user(username, email, password)
            return Response(data={"User created."}, status=200)
        else:
            return Response(data={"Invalid user or already created."}, status=400)


class UpdateProfileView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'

class CreateProfileView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):

        try:
            profile_serializer = ProfileSerializer(data={
                "user": self.request.user.pk,
                "name": request.data['name'],
                "email": request.data['email'],
                "course": request.data['course'],
                "user_permissions": request.data['user_permissions'],
                "code": request.data['code']
            })
            if profile_serializer.is_valid():
                profile_serializer.save()
                return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={"Error creating profile.", str(e)}, status=400)


class SelectedProfileView(APIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )

    def get(self, request):

        try:
            selected_profile = Profile.objects.get(user=self.request.user.pk)
            dict_selected_profile = model_to_dict(selected_profile)
            print(dict_selected_profile)
            return Response(data={
                "created": True,
                "data": dict_selected_profile
            }, status=200)

        except Exception as ex:
            return Response(data={
                "created": False,
                "data": {
                    "name": None,
                    "email": self.request.user.email,
                    "course": None,
                    "user_permissions": None,
                    "code": None
                }
            }, status=200)