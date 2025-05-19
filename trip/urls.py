from django.urls import path
from .views import *

urlpatterns = [
    path('create', createtripview.as_view(), name='trip-create'),
    path('createmuti', createmultipletripsview.as_view(), name='trip-create'),
    path('update/<int:pk>', updatetripview.as_view(), name='trip-update'),
    path('active/<int:pk>', UpdateTripIsActiveView.as_view(), name='trip-active'),
    path('delete/<int:pk>/', deletetripview.as_view(), name='delete'),
    path('bydate/', tripbydateview.as_view(), name='trip-by-date'),
    path('bytimeonday/', tripbytimeondayview.as_view(), name='trip-by-time-on-day'),
    path('byroute/', tripbyroutebiew.as_view(), name='trip-by-route'),
    path('<int:pk>/start/', starttripview.as_view(), name='trip-start'),
]
