from django.urls import path, include
from .views import *
urlpatterns = [
    path('create', createrouteview.as_view(), name='create'),
    path('update/<int:pk>/', updaterouteview.as_view(), name='update'),
    path('delete/<int:pk>/', deleterouteview.as_view(), name='delete'),
    path('getroute/<int:id>/', getroutebyidview, name='get'),
    path('list', listrouteview.as_view(), name='list'),
]