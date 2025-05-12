from django.urls import path
from .views import dashboard_view, buyer_dashboard, seller_dashboard, producer_profile, consumer_profile

# app_name = 'dashboard'
urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('buyer/', buyer_dashboard, name='buyer_dashboard'),
    path('seller/', seller_dashboard, name='seller_dashboard'),
    # path('producer/<str:wallet_address>/', producer_profile, name='producer_profile'),
    path('producer_profile/<str:address>/', producer_profile, name='producer_profile'),
    path('consumer/<str:wallet_address>/', consumer_profile, name='consumer_profile'),
] 
