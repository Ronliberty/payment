from django.urls import path
from .views import DepositMoneyView, SendMoneyView, VerifyOTPView, WithdrawMoneyView


app_name = 'payment'
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw'),
    path('send/', SendMoneyView.as_view(), name='send_money'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
