from django.urls import path
from .views import   ProfileView, HelpView, NotificationsView, RedirectAfterLoginView, CustomUserSignupView
from django.contrib.auth.views import LogoutView

app_name = 'custom'

urlpatterns = [

    path('profile/', ProfileView.as_view(), name='profile-settings'),
    path('help/', HelpView.as_view(), name='help-settings'),

    path('notify/', NotificationsView.as_view(), name='notify-settings'),
    path('redirect/', RedirectAfterLoginView.as_view(), name='redirect_after_login'),
    path("signup/", CustomUserSignupView.as_view(), name="account_signup"),


]

