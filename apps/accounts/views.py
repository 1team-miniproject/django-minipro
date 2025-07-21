from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer


class AccountListCreateApiView(APIView):  # 계좌 목록 조회 , 생성을 처리함
    @extend_schema(
        summary="현재 로그인된 사용자의 계좌 목록 조회",
        description="인증된 사용자가 소유한 모든 계좌의 목록을 조회합니다.",
        responses={
            200: AccountSerializer(many=True),  # 성공 시 계좌 목록 반환
            201: {"description": "성공적으로 생성"},
            400: {"description": "잘못된 요청 데이터 (Bad Request)"},
            401: {"description": "인증 정보 없음 (Unauthorized)"},
        },
        tags=["accounts"],  # Swagger UI에서 뷰를 그룹화하는 태그
    )
    def get(self, request):  # 계좌 목록 조회
        # 유저의 계좌 목록 조회 API 작성
        pass

    @extend_schema(
        summary="새로운 계좌 생성",
        description="현재 로그인된 사용자를 위한 새로운 계좌를 생성합니다.",
        request=AccountSerializer,  # 요청 본문의 스키마를 AccountSeriailzer로 지정
        responses={
            201: AccountSerializer,  # 성공 시 생성된 계좌 정보 반환
            400: {"description": "잘못된 요청 데이터 (Bad Request)"},
            401: {"description": "인증 정보 없음 (Unauthorized)"},
        },
    )
    def post(self, request):  # 새 계좌 생성
        # 계좌 생성 API 작성
        pass


class AccountDeleteAPIView(APIView):  # 계좌 삭제 처리
    @extend_schema(
        summary="계좌 삭제",
        description="현재 로그인된 사용자의 계좌를 삭제합니다.",
        request=AccountSerializer,  # 요청 본문의 스키마를 AccountSeriailzer로 지정
        responses={
            201: AccountSerializer,  # 성공 시 생성된 계좌 정보 반환
            400: {"description": "잘못된 요청 데이터 (Bad Request)"},
            401: {"description": "인증 정보 없음 (Unauthorized)"},
            404: {"description": "거래 내역을 찾을 수 없음"},
        },
        tags=["accounts"],
    )
    def delete(self, request, pk): # 계좌 삭제
        # 계좌 삭제 API 작성
        pass