from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class UserMeApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response({'message': 'DEleted successfully'}, status=status.HTTP_200_OK)


class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'email', 'nickname', 'phone_number')
        return Response(users)

# 회원가입
class ResisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 되었습니다"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            refresh = RefreshToken.for_user(user)

            return Response({"access": str(refresh.access_token),
                             "refresh": str(refresh),
                             "message": '로그인 성공'
                             }, status=status.HTTP_200_OK)
        return Response({"error": "이메일 또는 비밀번호가 틀렸습니다"}, status=status.HTTP_400_BAD_REQUEST)

# 로그아웃
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({'error': 'Refresh token이 필요합니다'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': '유효하지 않는 토큰입니다'},status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)

