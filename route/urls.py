from django.urls import path, include
from .views import *
urlpatterns = [
    path('create', CreateRouteView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateRouteView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteRouteView.as_view(), name='delete'),
    path('getroute/<int:id>/', get_route_by_id_view, name='get'),
    path('list', ListRouteView.as_view(), name='list'),
]