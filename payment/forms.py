from django import forms
from .models import Transaction

class DepositForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1.00)
    phone_number = forms.CharField(max_length=20, help_text="Enter Mpesa number for deposit")
    class Meta:
        model = Transaction
        fields = ['amount', 'phone_number']




class WithdrawForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        help_text="Enter your mobile number (e.g. M-Pesa number)"
    )

    class Meta:
        model = Transaction
        fields = ['phone_number', 'amount']


class SendForm(forms.ModelForm):
    recipient_email = forms.EmailField(help_text="Enter Email")

    class Meta:
        model = Transaction
        fields = ['recipient_email', 'amount']  # Add recipient_email here


class PaymentRequestForm(forms.Form):
    merchant_email = forms.EmailField(
        label="Merchant Email",
        help_text="Enter the email of the merchant"
    )
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label="Amount",
        help_text="Enter the amount to pay"
    )