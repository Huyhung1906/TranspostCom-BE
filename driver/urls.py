from django.urls import path, include
from .views import *
urlpatterns = [
    path('create/', CreateDriverView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateDriverView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteDriverView.as_view(), name='delete'),
    path('getdriver/<int:id>/', get_driver_by_id_view, name='get'),
    path('list', ListDriverView.as_view(), name='list'),
]