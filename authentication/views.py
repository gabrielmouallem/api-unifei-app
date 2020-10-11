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
import pdfplumber as pdf

def return_weekday(index):
    if index == 1:
        return "1#Domingo"
    if index == 2:
        return "2#Segunda"
    if index == 3:
        return "3#Terça"
    if index == 4:
        return "4#Quarta"
    if index == 5:
        return "5#Quinta"
    if index == 6:
        return "6#Sexta"
    if index == 7:
        return "7#Sábado"

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def extract_data(first_table, second_table):
    table = []
    first_table_result = []
    flag = True
    for row_index, row in enumerate(first_table):
        if "" in row:
            for column_index, column in enumerate(row):
                if column != "":
                    place_to_append = table[row_index - 1][column_index]
                    table[row_index - 1][column_index] = place_to_append + column
                    # Deletar a row_index
        else:
            table.append(row)
    # print(table)
    for row in table:
        if "" in row:
            print("jumped row.")
        else:
            data = {}
            if flag == True:
                flag = False
                continue
            if ('SUPERV' in row[0]) or ('FINAL' in row[0]):
                continue
            if 'ORIENTADOR' in row[1]:
                # print('b')
                continue
            if not row[4]:
                continue
            data['codigo_horario'] = row[4]
            data['local'] = row[1].split()[-1]
            data['codigo'] = row[0]
            if data:
                first_table_result.append(data)

    for row_index, row in enumerate(second_table):
        if row_index > 0:
            for column_index, column in enumerate(row):
                time = row[0]
                for index, table in enumerate(first_table_result):
                    if table['codigo'] == column:
                        if not "horario" in first_table_result[index]:
                            first_table_result[index]['horario'] = str(column_index) +"#" + time
                        else:
                            first_table_result[index]['horario'] = first_table_result[index]['horario'] + " $" + str(column_index) +"#" + time
                        if not "dia_da_semana" in first_table_result[index]:
                            first_table_result[index]['dia_da_semana'] = return_weekday(column_index)
                        else:
                            if str(first_table_result[index]['dia_da_semana']).find(return_weekday(column_index)):
                                first_table_result[index]['dia_da_semana'] = first_table_result[index]['dia_da_semana'] + " $" + return_weekday(column_index)
                                first_table_result[index]['dia_da_semana'] = ' '.join(unique_list(first_table_result[index]['dia_da_semana'].split()))

    return (first_table_result)


class SendPdfView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def post (self, request):
        try:

            # data = request.data['data']
            # with open(os.path.expanduser('./myschedule.pdf'), 'wb') as fout:
            #     fout.write(base64.b64decode(data))

            # Caminho do arquivo
            path = './myschedule.pdf'
            reader = pdf.open(path)
            page = reader.pages[0]
            first_table_data = page.extract_tables()[0]
            second_table_data = page.extract_tables()[1]

            data = extract_data(first_table_data, second_table_data)
            # print(data)
            return Response(data={"data": data})

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