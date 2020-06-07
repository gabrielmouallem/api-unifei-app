import json

from django.contrib.auth.models import User, UserManager
from rest_framework.generics import CreateAPIView
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
        print(body)

        if not body.get('method'):
            return Response(status=400)

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
