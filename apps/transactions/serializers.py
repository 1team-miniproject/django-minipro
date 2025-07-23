from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Transaction


class TransactionSerializer(ModelSerializer):
    balance_after_transaction = IntegerField(default=0)
    class Meta:
        model=Transaction
        fields='__all__'