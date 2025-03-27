from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from payment.models import Wallet, Transaction

class BaseDashboardView(LoginRequiredMixin, TemplateView):
    group_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name=self.group_name).exists():
            messages.error(request, "You are not authorized to access this page.")
            return redirect('base:index')
        return super().dispatch(request, *args, **kwargs)


class ManagerDashboard(BaseDashboardView):
    template_name = 'dashboard/manger_dash.html'
    group_name = 'manager'

class UserDashboardView(BaseDashboardView):
    template_name = 'dashboard/user_dash.html'
    group_name = 'default'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wallet'] = Wallet.objects.get(user=self.request.user)
        context['transactions'] = Transaction.objects.filter(
            sender=self.request.user
        ).order_by('-timestamp')[:5]
        return context
