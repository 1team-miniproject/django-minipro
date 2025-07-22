import pytest
from apps.accounts.serializers import AccountSerializer
from apps.users.models import User
from apps.accounts.models import BANK_CODES, ACCOUNT_TYPE

pytestmark = pytest.mark.django_db

def test_account_serializer_valid_data():
    user = User.objects.create(name = 'test', email = 'test@example.com', password = 'dkanfjs1!')

    data = {
        'user_id': user.id,
        'account_number' : '12345567',
        'bank_code': '088',
        'account_type': 'SAVING',
        'balance': '10000.00'
    }

    serializer = AccountSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    account = serializer.save()

    assert account.account_number == data['account_number']
    assert str(account.balance) == data['balance']

def test_account_serializer_invalid_bank_code():
    user = User.objects.create(name = 'test', email = 'test@example.com', password = 'dkanfjs1!')

    data = {

        'user_id': user.id,
        'account_number': '12345567',
        'bank_code': '999',
        'account_type': 'SAVING',
        'balance': '5000.00'
    }

    serializer = AccountSerializer(data=data)
    assert not serializer.is_valid()
    assert 'bank_code' in serializer.errors

def test_account_serializer_missing_required_fields():
    user = User.objects.create(name = 'test', email = 'test@example.com', password = 'dkanfjs1!')

    data = {
        'user_id': user.id,
        'bank_code': '088',
        'account_type': 'SAVING',
        'balance': '5000.00'
    }
    serializer = AccountSerializer(data=data)
    assert not serializer.is_valid()
    assert 'account_number' in serializer.errors