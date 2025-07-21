from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account  # Account 모델을 직렬화
        fields = "__all__"