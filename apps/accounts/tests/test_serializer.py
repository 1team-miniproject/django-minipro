import pytest
from apps.accounts.models import Account
from rest_framework.test import APIClient
from apps.accounts.serializers import AccountSerializer
from apps.users.models import User
from apps.accounts.models import BANK_CODES, ACCOUNT_TYPE
from django.urls import reverse

pytestmark = pytest.mark.django_db

@pytest.fixture
def drf_client():
    return APIClient()
@pytest.fixture
def user():
    return User.objects.create_user(
        email = 'test@example.com',
        password = 'testpass123!',
        name = 'test',
        nickname = 'tester',
        phone_number = '123456789',
    )

@pytest.fixture
def auth_client(drf_client, user):
    drf_client.force_authenticate(user=user)
    return drf_client

def test_create_account(auth_client, user):
    url = reverse('accounts:account-list-create')
    data = {
        'account_number' : '1234567',
        'bank_code': '088',
        'account_type': 'SAVING',
        'balance': '50000.00'
    }

    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert Account.objects.filter(user_id=user, account_number='1234567').exists()

def test_get_account_list(auth_client, user):
    # 사전 계좌 생성
    Account.objects.create(
    user_id = user,
    account_number = '1234567',
    bank_code = '088',
    account_type = 'CHECKING',
    balance = '100000.00'
    )
    url = reverse('accounts:account-list-create')
    response = auth_client.get(url)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) == 1
    assert response.data[0]['account_number'] == '1234567'


def test_delete_account(auth_client, user):
    account = Account.objects.create(
        user_id=user,
        account_number='999999999',
        bank_code='088',
        account_type='SAVING',
        balance='10000.00'
    )
    url = reverse('accounts:account-delete', kwargs={'pk': account.pk})
    response = auth_client.delete(url)

    assert response.status_code == 204
    assert not Account.objects.filter(pk=account.pk).exists()

