import csv
from PIL.ImagePalette import random
from django.db import transaction as db_transaction
from django.views.generic import CreateView, ListView
from decimal import Decimal
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet, Transaction
from .forms import DepositForm, SendForm, WithdrawForm, PaymentRequestForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from django.http import HttpResponse

from django.urls import reverse_lazy

from django.core.mail import send_mail

from django.contrib import messages

from django.views import View
import random
User = get_user_model()




class DepositMoneyView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'payment/deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        # Set transaction details
        form.instance.receiver = self.request.user  # Deposit goes to current user
        form.instance.transaction_type = 'deposit'
        form.instance.status = 'completed'  # REQUIRED to trigger wallet update

        # Save transaction and process
        response = super().form_valid(form)

        # Optional: Force immediate processing if async issues exist
        self.object.process_transaction()

        return response





class WithdrawMoneyView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'payment/withdraw.html'
    form_class = WithdrawForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        user = self.request.user
        phone_number = form.cleaned_data['phone_number']
        amount = form.cleaned_data['amount']

        # Ensure the amount is a Decimal (for arithmetic compatibility)
        amount = Decimal(amount)

        # Get or create the user's wallet
        wallet, _ = Wallet.objects.get_or_create(user=user)

        # Check if the user has sufficient balance
        if wallet.balance < amount:
            messages.error(self.request, "Insufficient balance.")
            return self.form_invalid(form)

        with db_transaction.atomic():
            # Deduct the amount from the user's wallet
            wallet.balance -= amount
            wallet.save()

            # Create a withdrawal transaction.
            # In this case, no 'receiver' user exists because funds are going to a phone number.
            Transaction.objects.create(
                sender=user,
                receiver=None,  # No receiver account for withdrawal
                amount=amount,
                transaction_type='withdraw',
                phone_number=phone_number,
                status='pending'  # You can mark as pending if further processing is needed
            )

        messages.success(self.request, "Withdrawal request submitted successfully.")
        return super().form_valid(form)


class SendMoneyView(LoginRequiredMixin, CreateView):
    template_name = 'payment/send_money.html'
    form_class = SendForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        sender = self.request.user
        recipient_email = form.cleaned_data['recipient_email']

        amount = form.cleaned_data['amount']

        amount = Decimal(amount)
        recipient = get_object_or_404(User, email=recipient_email)
        sender_wallet, _ = Wallet.objects.get_or_create(user=sender)  # ✅ Create if missing
        recipient_wallet, _ = Wallet.objects.get_or_create(user=recipient)  # ✅ Create if missing

        # Check if sender has enough balance
        if sender_wallet.balance < amount:
            messages.error(self.request, "Insufficient funds.")
            return self.form_invalid(form)

        otp = random.randint(10000, 999999)
        self.request.session ['otp'] = otp
        self.request.session['recipient_email'] = recipient_email
        self.request.session['amount'] = str(amount)

        with db_transaction.atomic():
            transaction = Transaction.objects.create(
                sender=sender,
                receiver=recipient,
                amount=amount,
                transaction_type='transfer',
                status='completed'  # Mark as completed to trigger process_transaction
            )

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount
        sender_wallet.save()
        recipient_wallet.save()

        # Process transaction to update wallets
        transaction.process_transaction()

        send_mail(
            subject='otp for payment',
            message=f'Your otp is {otp}',
            from_email='dantezmalusi254@gmail.com',
            recipient_list=[self.request.user.email],
            fail_silently=False,
        )
        messages.info(self.request, 'otp has been sent to your email')
        return super().form_valid(form)




class PaymentRequestView(LoginRequiredMixin, FormView):
    model = Transaction
    template_name = 'payment/payment.html'
    form_class = PaymentRequestForm
    success_url = reverse_lazy('dashboard:user_dashboard')
    def form_valid(self, form):
        merchant_email = form.cleaned_data['merchant_email']
        amount = form.cleaned_data['amount']
        try:
            merchant_user = User.objects.get(email=merchant_email)  # Renamed variable for clarity
            if not merchant_user.groups.filter(name='merchants').exists():
                messages.error(self.request, 'Merchant with that email does not exist.')
                return self.form_invalid(form)
        except User.DoesNotExist:
            messages.error(self.request, 'Merchant not found.')
            return self.form_invalid(form)

        otp = random.randint(10000, 999999)
        self.request.session['otp'] = otp
        self.request.session['merchant_email'] = merchant_email
        self.request.session['amount'] = str(amount)
        self.request.session['payment'] = True

        trans = Transaction.objects.create(
            sender=self.request.user,
            receiver=merchant_user,
            amount=amount,
            transaction_type='payment_request',  # Changed here
            status='completed'
        )
        trans.process_transaction()

        send_mail (
            subject='otp for payment',
            message=f'Your otp for payment completion',
            from_email='dantezmalusi254@gmail.com',
            recipient_list=[self.request.user.email],
            fail_silently=False
        )
        messages.info(self.request, 'Otp has been sent to your email')
        return super().form_valid(form)

class VerifyOTPView(LoginRequiredMixin, View):
    template_name = 'payment/verify_otp.html'
    success_url = reverse_lazy('dashboard:user_dashboard')

    def post(self, request):
        input_otp = request.POST.get('otp')
        if str(request.session.get('otp')) == input_otp:
            if request.session.get('payment'):
                Transaction.objects.create(user=request.user, transaction_type='payment',
                                           amount=request.session['merchant_email'])
                del request.session['payment']
            else:
                Transaction.objects.create(user=request.user, transaction_type='send', amount=request.session['amount'],
                                           to_email=request.session['reciever_email'])
            messages.success(request, 'Transaction successful.')
            return super().form_valid(request)

        messages.error(request, 'Invalid otp. Try again')
        return self.form_invalid(request)


class MerchantPaymentsView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'payment/payments.html'
    context_object_name = 'transactions'


    def get_queryset(self):
        """
        Fetch only completed payment requests where the logged-in user is the receiver (merchant).
        """
        return Transaction.objects.filter(
            receiver=self.request.user,
            transaction_type='payment_request',
            status='completed'
        ).order_by('-timestamp')

def export_merchant_payments_csv(request):
    """
    Generate a CSV report of payments received by the merchant.
    """
    transactions = Transaction.objects.filter(
        receiver=request.user,
        transaction_type='payment_request',
        status='completed'
    ).order_by('-timestamp')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="merchant_payments.csv"'

    writer = csv.writer(response)
    writer.writerow(['Sender', 'Amount', 'Status', 'Date'])

    for transaction in transactions:
        writer.writerow([
            transaction.sender.email if transaction.sender else 'Anonymous',
            transaction.amount,
            transaction.status,
            transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response


class MerchantWithdrawView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'payment/merchant_withdraw.html'  # Create this template
    form_class = WithdrawForm
    success_url = reverse_lazy('dashboard:machant-dashboard')  # Update with the correct URL

    def form_valid(self, form):
        merchant = self.request.user
        phone_number = form.cleaned_data['phone_number']
        amount = form.cleaned_data['amount']

        # Ensure the amount is Decimal
        amount = Decimal(amount)

        # Check if the user is a merchant
        if not merchant.groups.filter(name='merchants').exists():
            messages.error(self.request, "Unauthorized access.")
            return self.form_invalid(form)

        # Get the merchant's wallet
        wallet, _ = Wallet.objects.get_or_create(user=merchant)

        # Check balance
        if wallet.balance < amount:
            messages.error(self.request, "Insufficient balance.")
            return self.form_invalid(form)

        with db_transaction.atomic():
            # Deduct the amount from the wallet
            wallet.balance -= amount
            wallet.save()

            # Create withdrawal transaction
            Transaction.objects.create(
                sender=merchant,
                receiver=None,  # No receiver for withdrawal
                amount=amount,
                transaction_type='withdrawal',  # Ensure correct transaction type
                phone_number=phone_number,
                status='pending'  # Mark as pending for further processing
            )

        messages.success(self.request, "Withdrawal request submitted successfully.")
        return super().form_valid(form)



def wallet_balance_processor(request):
    """Make wallet balance available in all templates."""
    if request.user.is_authenticated:
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        return {'wallet_balance': wallet.balance}
    return {'wallet_balance': 0}