from django.urls import path
from . views import MerchantDashboard, UserDashboardView, ManagerDashboard


app_name = 'dashboard'
urlpatterns = [
    path('user_dashboard/', UserDashboardView.as_view(), name='user_dashboard' ),
    path('machant/', MerchantDashboard.as_view(), name='machant-dashboard'),
    path('manager/', ManagerDashboard.as_view(), name='manager-dashboard'),

]