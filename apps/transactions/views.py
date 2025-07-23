from rest_framework.views import APIView
from .models import Transaction
from rest_framework import status
from rest_framework.response import Response
from .serializers import TransactionSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

class TransactionAPIView(APIView):
    @extend_schema(
        summary="거래 생성",
        description="입출금 거래 생성",
        # 새 거래내역을 생성하고, 연결된 계좌의 잔액을 업데이트.
        # 
        request=TransactionSerializer,
        responses={
            201: OpenApiResponse(response=TransactionSerializer, description="거래 생성 성공"),

            400: OpenApiResponse(description="잔액 부족 또는 잘못된 접근"),
        },
    )
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

    @extend_schema(
        summary="거래 조회",
        description="로그인 유저의 전체 거래내역 조회",
        responses={
            200: OpenApiResponse(response=TransactionSerializer(many=True),description="거래 목록 조회 성공"),
        },
    )

    # 거래 조회
    def get(self, request):
        transactions=Transaction.objects.filter(account_id__user_id=request.user)
        serializer=TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransactionDetailAPIView(APIView):
    @extend_schema(
        summary="거래 수정",
        description="특정 거래 내역을 수정",
        request=TransactionSerializer,
        responses={
            200: OpenApiResponse(response=TransactionSerializer, description="거래 수정 성공"),
            404: OpenApiResponse(description="입력값이 잘못되었거나 거래를 찾을 수 없음"),
        },
    )
    # 거래 수정
    def put(self, request, pk):
        obj = Transaction.objects.get(pk=pk)
        user_data = request.data
        serializer = TransactionSerializer(obj, user_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="거래 삭제",
        description="특정 거래 내역을 삭제",
        responses={
            204: OpenApiResponse(description="거래 삭제 성공"),
            404: OpenApiResponse(description="거래를 찾을 수 없음"),
        },
    )

    # 거래 삭제
    def delete(self, request, pk):
        obj = Transaction.objects.get(pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
