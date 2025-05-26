from django.urls import path
from .views import *

urlpatterns = [
    path('create', CreateTicketView.as_view(), name='create-ticket'),
    path('getlist/<int:trip_id>', GetListTicketbyTrip.as_view(), name='get-list'),
    path('<int:pk>/detail/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<int:pk>/update/', UpdateTicketView.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', DeleteTicketView.as_view(), name='ticket-delete'),
]
    