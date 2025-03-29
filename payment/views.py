from PIL.ImagePalette import random

from django.views.generic import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet, Transaction
from .forms import DepositForm, SendForm, WithdrawForm, PaymentRequestForm

from django.contrib.auth import get_user_model
from django.views.generic.edit import FormView

from django.urls import reverse_lazy

from django.core.mail import send_mail

from django.contrib import messages

from django.views import View
import random
User = get_user_model()




class DepositMoneyView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'dashboard/user_dash.html'
    form_class = DepositForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.transaction_type = 'deposit'
        return super().form_valid(form)

class WithdrawView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'dashboard/user_dash.html'
    form_class = WithdrawForm
    success_url = reverse_lazy('dashboard:user_dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.user = 'withdraw'
        return super().form_valid(form)



class WithdrawMoneyView(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'dashboard/user_dash.html'
    form_class = WithdrawForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.transaction_type = 'withdraw'

        return super().form_valid(form)


class SendMoneyView(LoginRequiredMixin, CreateView):
    template_name = 'dashboard/user_dash.html'
    form_class = SendForm
    success_url = reverse_lazy('dashboard:user_dashboard')

    def form_valid(self, form):
        receiver_email = form.cleaned_data ['receiver_email']
        amount = form.cleaned_data ['amount']
        otp = random.randint(10000, 999999)
        self.request.session ['otp'] = otp
        self.request.session['reciver_email'] = receiver_email
        self.request.session['amount'] = amount

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
    template_name = 'payment/pay.html'
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
        self.request.session['amount'] = amount
        self.request.session['payment'] = True

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

