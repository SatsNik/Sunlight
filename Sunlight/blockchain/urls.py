from django.urls import path
from .views import get_available_sellers, get_my_buying_history, get_my_selling_history, register_buyer_onchain, register_seller_onchain, buy_energy, update_price, update_energy

app_name = 'blockchain'
urlpatterns = [
    path('available-sellers/', get_available_sellers, name='available_sellers'),
    path('my-buying-history/', get_my_buying_history, name='my_buying_history'),
    path('my-selling-history/', get_my_selling_history, name='my_selling_history'),
    path('register-buyer/', register_buyer_onchain, name='register_buyer_onchain'),
    path('register-seller/', register_seller_onchain, name='register_seller_onchain'),
    path('buy-energy/', buy_energy, name='buy_energy'),
    path('update-price/', update_price, name='update_price'),
    path('update-energy/', update_energy, name='update_energy'),
] 
