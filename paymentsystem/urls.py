from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('custom/', include('custom.urls')),
    path('dashboard', include('dashboard.urls')),
    path('payment/', include('payment.urls')),

    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)