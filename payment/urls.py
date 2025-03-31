from django.urls import path
from .views import DepositMoneyView, SendMoneyView, VerifyOTPView, WithdrawMoneyView, PaymentRequestView, MerchantPaymentsView, export_merchant_payments_csv, MerchantWithdrawView


app_name = 'payment'
urlpatterns = [
    path('deposit/', DepositMoneyView.as_view(), name='deposit'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw'),
    path('send/', SendMoneyView.as_view(), name='send_money'),
    path('pay/', PaymentRequestView.as_view(), name='pay_merchant'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('merchant/payments/', MerchantPaymentsView.as_view(), name='merchant_payments'),
    path('merchant/payments/export/', export_merchant_payments_csv, name='export_merchant_payments_csv'),
    path('merchant/withdraw/', MerchantWithdrawView.as_view(), name='merchant_withdraw'),

]
