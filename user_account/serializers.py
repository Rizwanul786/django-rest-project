from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            # print("===>>",user)
            if user:
                if user.is_active:
                    attrs['user'] = user
                    return attrs
                else:
                    msg = 'User is inactive'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg)