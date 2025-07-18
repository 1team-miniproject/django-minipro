from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenObtainPairView )
from .views import ResisterAPIView, LoginAPIView, LogoutAPIView,UserListAPIView, UserMeApiView

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('me/', UserMeApiView.as_view(), name='user=profile'),
    path('signup/', ResisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/',TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
]