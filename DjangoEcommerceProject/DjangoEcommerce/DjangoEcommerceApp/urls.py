# registration/urls.py
from django.urls import path
from .views import registration_view, registration_success_view, homepage, login_with_otp

urlpatterns = [
    path('home/', homepage, name='homepage'),
    path('register/', registration_view, name='registration'),
    path('registration-success/', registration_success_view, name='registration_success'),
    path('login/', login_with_otp, name='login_with_otp'),
]
