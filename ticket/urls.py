from django.urls import path
from .views import *

urlpatterns = [
    path('create', createticketview.as_view(), name='create-ticket'),
    path('getlist/<int:trip_id>', getticketbylist.as_view(), name='create-ticket'),
    path('<int:pk>/detail/', ticketdetailview.as_view(), name='ticket-delete'),
    path('<int:pk>/update/', updateticketview.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', deletetticketview.as_view(), name='ticket-delete'),
]

