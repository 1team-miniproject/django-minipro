import pytest
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.users.serializer import RegisterSerializer
from apps.users.models import User
# User = get_user_model()

class DummyLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterTestRegisterSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    name = serializers.CharField()
    nickname = serializers.CharField()
    phone_number = serializers.CharField()


    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'name', 'nickname', 'phone_number')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User(**validated_data)


def test_register_serializer_valid():
    # client = APIClient()
    data = {
        "email" : "test11@gmail.com",
        "password" : "stringpass123!",
        "password2" : "stringpass123!",
        "name": "오즈",
        "nickname": "5즈",
        "phone_number" : "01012345678"
    }
    # response = client.post(reverse('signup'), data=data)
    # print(response.data)
    serializer = RegisterTestRegisterSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    # assert User.objects.filter(email='test11@gmail.com').exists()





def test_register_password_mismatch():
    # client = APIClient()
    data = {
        "email" : "test11@gmail.com",
        "password" : "test1",
        "password2" : "differentpass",
        "name": "오즈",
        "nickname": "5즈",
        "phone_number" : "01012345678"
    }
    serializer = RegisterTestRegisterSerializer(data=data)
    # response = client.post(reverse('signup'), data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors
    # assert "password" in response.data