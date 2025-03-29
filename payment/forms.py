from django import forms

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=1.00)
    phone_number = forms.CharField(max_length=20, help_text="Enter Mpesa number for deposit")

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    mpesa_number = forms.CharField(max_length=20, help_text="Enter Mpesa number for withdrawal")

class SendForm(forms.Form):
    recipient_email = forms.EmailField(help_text="Enter Email")
    amount = forms.DecimalField(max_digits=12, decimal_places=2)


class PaymentRequestForm(forms.Form):
    merchant_email = forms.EmailField(help_text="Enter Email")
    amount = forms.DecimalField(max_digits=12, decimal_places=2)