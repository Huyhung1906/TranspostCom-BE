from django.urls import path
from .views import *

urlpatterns = [
    path('create', CreateTripView.as_view(), name='trip-create'),
    path('createmuti', CreateMutiTripView.as_view(), name='trip-create'),
    path('update/<int:pk>', UpdateTripView.as_view(), name='trip-update'),
    path('active/<int:pk>', UpdateTripIsActiveView.as_view(), name='trip-active'),
    path('delete/<int:pk>/', DeleteTripView.as_view(), name='delete'),
    path('bydate/', TripbyDateView.as_view(), name='trip-by-date'),
    path('bytimeonday/', TripbyTimeonDayView.as_view(), name='trip-by-time-on-day'),
    path('byroute/', TripbyRouteView.as_view(), name='trip-by-route'),
    path('<int:pk>/start/', StartTripView.as_view(), name='trip-start'),
    path('', TripbyRouteDateView.as_view(), name='trip-list'),
    path('info/<int:trip_id>/', TripDetailAPIView.as_view(), name='trip-detail'),
]
