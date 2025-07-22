import pytest
from apps.accounts.models import Account
from apps.transactions.models import Transaction
from apps.accounts.serializers import AccountSerializer
from rest_framework import serializers
from django.utils import timezone
from decimal import Decimal
from apps.users.models import User

pytestmark = pytest.mark.django_db

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

@pytest.fixture
def user():
    return User.objects.create_user(email='test@example.com', name = 'tester', password = 'dkanfjs1!')

@pytest.fixture
def account(user):
    return Account.objects.create(
        user_id = user,
        account_number = '1234565678',
        bank_code = '088',
        account_type = 'SAVING',
        balance = '10000.00',
    )

def test_transactions_create_deposit(account):
    data = {
        'id': 1,
    'account_id' : account.id,
    'amount' : '50000.00',
    'balance_after_transaction': '150000.00',
    'description': '월급 입금',
    'io_type': 'DEPOSIT',
    'transaction_type': 'TRANSFER'
    }

    serializer = TransactionSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    transaction = serializer.save()
    assert transaction.io_type == 'DEPOSIT'
    assert transaction.balance_after_transaction == Decimal('150000.00')
    assert transaction.created_at is not None


def test_transaction_filter_by_io_type(account):
    Transaction.objects.create(
        id = 2,
        account_id = account,
        amount = '30000.00',
        balance_after_transaction = '70000.00',
        description = '쇼핑',
        io_type = 'WITHDRAW',
        transaction_type = 'CARD'
    )

    Transaction.objects.create(
        id = 3,
        account_id = account,
        amount = '50000.00',
        balance_after_transaction = '120000.00',
        description = '보너스',
        io_type = 'DEPOSIT',
        transaction_type = 'TRANSFER'
    )

    # 필터링 : 입금
    deposits = Transaction.objects.filter(io_type = 'DEPOSIT', amount__gte=30000)
    assert deposits.count() == 1
    assert deposits.first().description == '보너스'

def test_transaction_update(account):
    transaction = Transaction.objects.create(
        id = 4,
        account_id = account,
        amount = '20000.00',
        balance_after_transaction = '80000.00',
        description = '수정 전',
        io_type = 'WITHDRAW',
        transaction_type = 'CARD'
    )

    transaction.description = '수정 후'
    transaction.amount = Decimal('30000.00')
    transaction.save()

    update = Transaction.objects.get(id=transaction.id)
    assert update.description == '수정 후'
    assert update.amount == Decimal('30000.00')

def test_transaction_delete(account):
    transaction = Transaction.objects.create(
        id = 5,
        account_id = account,
        amount = '15000.00',
        balance_after_transaction = '90000.00',
        description = '삭제 할 거래',
        io_type = 'WITHDRAW',
        transaction_type = 'ATM'
    )

    transaction_id = transaction.id
    transaction.delete()

    assert not Transaction.objects.filter(id=transaction_id).exists()

def test_get_all_transactions_for_user(account, user):
    Transaction.objects.create(
        id = 6,
        account_id = account,
        amount = '10000.00',
        balance_after_transaction = '90000.00',
        description = '거래1',
        io_type = 'WITHDRAW',
        transaction_type = 'ATM'
    )

    Transaction.objects.create(
        id = 7,
        account_id = account,
        amount = '30000.00',
        balance_after_transaction = '120000.00',
        description = '거래2',
        io_type = 'WITHDRAW',
        transaction_type = 'TRANSFER'
    )

    transactions = Transaction.objects.filter(account_id__user_id = user)
    assert transactions.count() == 2