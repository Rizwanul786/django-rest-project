from django.contrib.auth import authenticate
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer,UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.create(user=user).key
        })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        # print(request.data)
        serializer = self.get_serializer(data=request.data)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        # super_users=User.objects.filter(is_superuser=True).values_list('username',flat=True)
        # print(super_users)
        return Response({"token": token.key,'username':user.username,"is_superuser":user.is_superuser})