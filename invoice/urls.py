from django.urls import path
from .views import *

urlpatterns = [
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('create-with-tickets/', InvoiceCreateWithTicketsView.as_view(), name='invoice-create-with-tickets'),
    path('list/', InvoiceListView.as_view(), name='invoice-list'),
    path('<int:pk>/detail/', InvoiceDetailView.as_view(), name='invoice-detail'),

    # Payment Transactions
    path('payments/create/', PaymentTransactionCreateView.as_view(), name='payment-create'),
    path('payments/list/', PaymentTransactionListView.as_view(), name='payment-list'),
]
