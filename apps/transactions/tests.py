from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.users.models import User
from apps.accounts.models import Account
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Transaction
from decimal import Decimal

class TransactionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', name = 'tester', password = 'dkanfjs1!')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.account=Account.objects.create(
            user_id = self.user,
            account_number = '1234565678',
            bank_code = '088',
            account_type = 'SAVING',
            balance = '10000.00',
        )

    def test_post_transaction(self):
        url = reverse("Transaction")
        data = {
            'account_id' : self.account.id,
            'amount' : 50000.00,
            'description': '월급 입금',
            'io_type': 'DEPOSIT',
            'transaction_type': 'TRANSFER'
        }
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['io_type'], 'DEPOSIT')
        self.assertEqual(Decimal(res.data['balance_after_transaction']), Decimal('60000.00'))
        self.assertIsNotNone(res.data['created_at'])

    def test_get_transactions(self):
        Transaction.objects.create(
            account_id=self.account,
            amount=30000.00,
            balance_after_transaction=70000.00,
            description='쇼핑',
            io_type='WITHDRAW',
            transaction_type='CARD'
        )
        Transaction.objects.create(
            account_id=self.account,
            amount=50000.00,
            balance_after_transaction=20000.00,
            description='보너스',
            io_type='DEPOSIT',
            transaction_type='TRANSFER'
        )
        url = reverse("Transaction")
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_put_transaction(self):
        transaction = Transaction.objects.create(
            account_id=self.account,
            amount=20000.00,
            balance_after_transaction=80000.00,
            description='수정 전',
            io_type='WITHDRAW',
            transaction_type='CARD'
        )
        url = reverse("Transaction-detail", kwargs={"pk": transaction.pk})
        data = {'description':'update_description',
                'amount':30000.00}
        res = self.client.put(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['description'], 'update_description')
        self.assertEqual(res.data['amount'], '30000.00')

    def test_delete_transaction(self):
        transaction = Transaction.objects.create(
            account_id=self.account,
            amount=15000.00,
            balance_after_transaction=90000.00,
            description='삭제 할 거래',
            io_type='WITHDRAW',
            transaction_type='ATM'
        )

        url = reverse("Transaction-detail", kwargs={"pk": transaction.pk})
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Transaction.objects.filter(id=transaction.pk).exists())
