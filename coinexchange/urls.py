from django.urls import path
from .views import *

app_name = 'coinexchange'

urlpatterns = [
    path('add_transaction/', add_transaction),
    path('get_transaction/', TransactionAPIView.as_view()),
    path('check_balance/', CheckBalanceAPIView.as_view()),
]