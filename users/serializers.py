from rest_framework import serializers

from . models import Profile
from django.contrib.auth.models import User
from . utils import SendMail

from typing import Dict, Any


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ['username','email',]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSerializer()
        field = ['full_name','phone','gender','image']


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    password1 = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)

    class Meta:
        model = Profile
        fields = ['full_name','phone','gender','image','email','username','password1','password2']
    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password does not match')
        return data
    
    def create(self, validated_data: Dict[str, Any]):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')

        user = User.objects.create_user(username=username,email=email,password=password)

        profile = Profile.objects.create(
            user = user,
            full_name = validated_data['full_name'],
            phone = validated_data['phone'],
            gender= validated_data['gender'],
            image = validated_data.get('image'),
        )
        SendMail(email,profile.full_name)
        return profile








