from django.urls import path
from .views import TransactionAPIView, TransactionDetailAPIView

urlpatterns = [
    path('', TransactionAPIView.as_view(), name='Transaction'),
    path('<int:pk>/', TransactionDetailAPIView.as_view(), name='Transaction-detail')
]