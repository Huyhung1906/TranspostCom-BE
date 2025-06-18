from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.InvoiceCreateWithTicketsView.as_view(), name='create-invoice'),
    path('hold/', views.HoldTicketView.as_view(), name='hold-ticket'),
    path('release/', views.ReleaseTicketView.as_view(), name='release-ticket'),
    path('vnpay-url/', views.VnpayPaymentUrlView.as_view(), name='vnpay-url'),
    path('vnpay-return/', views.vnpay_return, name='vnpay-return'),
    path('list/', views.UserInvoiceListView.as_view(), name='list'),
    path('lookup/', views.InvoiceLookupView.as_view(), name='invoice-lookup'),

]
