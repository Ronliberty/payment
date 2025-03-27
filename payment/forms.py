from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label="Amount")

class SendMoneyForm(forms.Form):
    recipient = forms.CharField(max_length=150, label="Recipient Username")
    amount = forms.DecimalField(max_digits=12, decimal_places=2, label="Amount")

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)
    number = forms.CharField(max_length=20, help_text="Enter phone or account number")

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")
