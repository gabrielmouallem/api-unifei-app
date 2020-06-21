import json

from django.conf import settings
from django.contrib.auth.models import User, UserManager
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from authentication.serializers import UserSerializer


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
