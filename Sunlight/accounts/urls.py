from django.urls import path
from .views import register_view, login_view, logout_view, forgot_password_view, verify_forgot_otp_view, reset_password_view
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('verify-forgot-otp/', verify_forgot_otp_view, name='verify_forgot_otp'),
    path('reset-password/', reset_password_view, name='reset_password'),
    path('dashboard/update_address/', views.update_address, name='update_address'),
] 
