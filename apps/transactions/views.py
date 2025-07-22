from rest_framework.views import APIView
from .models import Transaction
from rest_framework import status
from rest_framework.response import Response
from .serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated

class TransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 거래생성
    def post(self, request):
        serializer=TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account_obj=serializer.validated_data["account_id"]
        amount=serializer.validated_data["amount"]
        io_type=serializer.validated_data["io_type"]

        if io_type=="DEPOSIT":
            account_obj.balance+=amount
        elif io_type=="WITHDRAW":
            if account_obj.balance<amount:
                return Response({"error":"잔액 부족"},status=status.HTTP_400_BAD_REQUEST)
            account_obj.balance-=amount
        else:
            return Response({"error":"잘못된 접근"},status=status.HTTP_400_BAD_REQUEST)

        serializer.save(balance_after_transaction=account_obj.balance)
        account_obj.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 거래 조회 ( 전체 )
    def get(self, request):
        transactions=Transaction.objects.filter(account_id__user_id=request.user)
        serializer=TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # 거래 조회
    def get(self, request, pk):
        transaction=Transaction.objects.get(pk=pk)
        serializer=TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 거래 수정
    def put(self, request, pk):
        obj = Transaction.objects.get(pk=pk)
        user_data = request.data
        serializer = TransactionSerializer(obj, user_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 거래 삭제
    def delete(self, request, pk):
        obj = Transaction.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
