from django.urls import path, include
from .views import *
urlpatterns = [
    path('create', createvehicleview.as_view(), name='create'),
    path('update/<int:pk>/', updatevehicleview.as_view(), name='update'),
    path('delete/<int:pk>/', deletevehicleview.as_view(), name='delete'),
    path('getvehicle/<int:id>/', getvehiclebyidview, name='get'),
    path('list', listvehicleview.as_view(), name='list'),

]   