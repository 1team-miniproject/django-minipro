import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
@pytest.mark.django_db
def test_login_success():
    user = User.objects.create_user(
        email = 'login@example.com',
        password = 'loginpass123!',
        name = 'test',
        nickname = '로그인 유저',
        phone_number = '01012345678',
    )
    client = APIClient()
    data = {'email': 'login@example.com', 'password': 'loginpass123!'}
    response = client.post(reverse('login'), data=data)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
@pytest.mark.django_db
def test_logout_token_blacklisted():
    user = User.objects.create_user(
        email = 'logout@example.com',
        password = 'logout123!',
        name = '로그아웃',
        nickname = '유저',
        phone_number = '01012345678',
    )
    client = APIClient()
    login_res = client.post(reverse('login'), data={
        'email': 'logout@example.com',
        'password' : 'logout123!'
    })
    refresh_token = login_res.data['refresh']
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_res.data['access']}")
    logout_res = client.post(reverse('logout'), data={'refresh': refresh_token})
    assert logout_res.status_code == 200

    protected_res = client.get(reverse('user-profile'))
    assert protected_res.status_code in [401, 403]