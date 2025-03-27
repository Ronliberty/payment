from django.urls import path
from . views import ManagerDashboard, UserDashboardView


app_name = 'dashboard'
urlpatterns = [
    path('user_dashboard/', UserDashboardView.as_view(), name='user_dashboard' ),
    path('manager/', ManagerDashboard.as_view(), name='manager-dashboard'),

]