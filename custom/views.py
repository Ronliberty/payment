from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from allauth.account.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import CustomUserSignupForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from allauth.account.auth_backends import AuthenticationBackend
from allauth.account.utils import send_email_confirmation
from django.http import HttpResponseRedirect
from allauth.account.utils import complete_signup
from allauth.account.adapter import get_adapter





class RedirectAfterLoginView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        group_redirects = {
            'default': 'dashboard:user_dashboard',
            'manager': 'dashboard:manager-dashboard',
            'writer': 'dashboard:Writer-dashboard',
            'moderator': 'dashboard:mod-dash',
        }

        # Get user groups
        user_groups = set(user.groups.values_list('name', flat=True))

        # Check if user belongs to any mapped group
        for group, url in group_redirects.items():
            if group in user_groups:
                return redirect(url)

        # Check if user is a superuser
        if user.is_superuser:
            return redirect('dashboard:super-dash')

        # Fallback
        return redirect('base:index')


class CustomUserSignupView(FormView):

    template_name = "account/signup.html"
    form_class = CustomUserSignupForm
    success_url = reverse_lazy("account_email_verification_sent")

    def form_valid(self, form):
        print("✅ Form is valid - Processing signup")
        user = form.save()
        user.is_active = False  # Prevent login until email is confirmed
        user.save()

        # Trigger Allauth's email confirmation process
        return complete_signup(
            self.request,
            user,
            self.get_success_url(),
            signal_kwargs={"user": user},
        )


class ProfileView(TemplateView):
    template_name = 'custom_account/profile.html'


class HelpView(TemplateView):
    template_name = 'custom/help.html'





class NotificationsView(TemplateView):
    template_name = 'custom/notify.html'
