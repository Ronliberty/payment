from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet, Transaction
from .forms import DepositForm, SendMoneyForm, WithdrawalForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView
from .models import OTP
from .forms import OTPForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


User = get_user_model()

class DepositMoneyView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/user_dash.html'
    form_class = DepositForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def get_form_classes(self):
        return {
            'deposit_form': DepositForm,
            'withdraw_form': WithdrawalForm
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['deposit_form'] = DepositForm()
        context['withdraw_form'] = WithdrawalForm()
        context['wallet'] = Wallet.objects.get(user=request.user)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if 'deposit_submit' in request.POST:
            return self.handle_deposit(request)
        elif 'withdraw_submit' in request.POST:
            return self.handle_withdraw(request)
        else:
            return self.get(request, *args, **kwargs)

    def handle_deposit(self, request):
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            wallet = Wallet.objects.get(user=request.user)
            wallet.balance += amount
            wallet.save()
            Transaction.objects.create(
                receiver=request.user,
                amount=amount,
                transaction_type="deposit",
                status="completed"
            )
            return redirect(self.success_url)
        return self.form_invalid(form)

    def handle_withdraw(self, request):
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            phone_number = form.cleaned_data['phone_number']
            wallet = Wallet.objects.get(user=request.user)

            if wallet.balance < amount:
                form.add_error('amount', 'Insufficient funds')
                return self.form_invalid(form)

            wallet.balance -= amount
            wallet.save()

            Transaction.objects.create(
                sender=request.user,
                amount=amount,
                transaction_type="withdrawal",
                status="completed"
            )
            print(f"Withdrew {amount} to {phone_number}")
            return redirect(self.success_url)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(user=self.request.user)
        return context



class SendMoneyView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/user_dash.html'
    form_class = SendMoneyForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        recipient_username = form.cleaned_data['recipient']
        amount = form.cleaned_data['amount']
        sender_wallet = Wallet.objects.get(user=self.request.user)
        recipient = get_object_or_404(User, username=recipient_username)
        recipient_wallet = Wallet.objects.get(user=recipient)

        if sender_wallet.balance >= amount:
            sender_wallet.balance -= amount
            recipient_wallet.balance += amount
            sender_wallet.save()
            recipient_wallet.save()

            Transaction.objects.create(
                sender=self.request.user,
                receiver=recipient,
                amount=amount,
                transaction_type="transfer",
                status="completed"
            )
        else:
            form.add_error(None, "Insufficient funds")
            return self.form_invalid(form)

        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class WithdrawMoneyView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/user_dash.html'
    form_class = WithdrawalForm
    success_url = reverse_lazy('dashboard:user_dashboard')



class VerifyOTPView(LoginRequiredMixin, FormView):
    template_name = 'payment/verify_otp.html'
    form_class = OTPForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        user_otp = form.cleaned_data['otp']
        try:
            otp = OTP.objects.get(user=self.request.user, code=user_otp, is_used=False)
            otp.is_used = True
            otp.save()
        except OTP.DoesNotExist:
            form.add_error(None, "Invalid OTP")
            return self.form_invalid(form)

        return super().form_valid(form)