import pytest
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.users.serializer import RegisterSerializer
from apps.users.models import User


# User = get_user_model()

@pytest.mark.django_db
def test_register_api_success():
    client = APIClient()
    data = {
        "email" : "test11@gmail.com",
        "password" : "stringpass123!",
        "password2" : "stringpass123!",
        "name": "오즈",
        "nickname": "5즈",
        "phone_number" : "01012345678"
    }
    response = client.post(reverse('signup'), data=data)
    assert response.status_code == 201
    assert User.objects.filter(email='test11@gmail.com').exists()
    assert response.data['message'] == "회원가입 되었습니다"




@pytest.mark.django_db
def test_register_password_mismatch():
    client = APIClient()
    data = {
        "email" : "test11@gmail.com",
        "password" : "test1",
        "password2" : "differentpass",
        "name": "오즈",
        "nickname": "5즈",
        "phone_number" : "01012345678"
    }
    response = client.post(reverse('signup'), data)
    assert response.status_code == 400
    assert "password" in response.data