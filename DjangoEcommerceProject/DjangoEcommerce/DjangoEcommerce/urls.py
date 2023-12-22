# mysite/urls.py
from django.contrib import admin
from django.urls import path, include
from DjangoEcommerceApp.views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('DjangoEcommerceApp.urls')),
]
