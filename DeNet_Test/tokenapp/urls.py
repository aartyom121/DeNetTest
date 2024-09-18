# tokenapp/urls.py

from django.urls import path
from .views import get_balance_view, get_balance_batch_view, get_token_info_view, get_transaction_history_view, get_top_addresses_view, get_top_addresses_with_transactions_view

urlpatterns = [
    path('get_balance/', get_balance_view, name='get_balance'),
    path('get_balance_batch/', get_balance_batch_view, name='get_balance_batch'),
    path('get_token_info/', get_token_info_view, name='get_token_info'),
    path('get_transaction_history/', get_transaction_history_view, name='get_transaction_history'),
    path('get_top_addresses/', get_top_addresses_view, name='get_top_addresses'),
    path('get_top_addresses_with_transactions/', get_top_addresses_with_transactions_view, name='get_top_addresses_with_transactions'),
]
