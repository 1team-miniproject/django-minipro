from django.db import models
from apps.common.models import BaseModel

TRANSACTION_IO_TYPE_CHOICES = [
    ("DEPOSIT", "입금"),
    ("WITHDRAW", "출금"),
]


TRANSACTION_METHOD_CHOICES = [
    ("ATM", "ATM 거래"),
    ("TRANSFER", "계좌이체"),
    ("AUTOMATIC_TRANSFER", "자동이체"),
    ("CARD", "카드결제"),
    ("INTEREST", "이자"),
]

class Transaction(BaseModel):
    id = models.BigAutoField(primary_key=True)
    account_id = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    io_type = models.CharField(max_length=10, choices=TRANSACTION_IO_TYPE_CHOICES)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_METHOD_CHOICES)
