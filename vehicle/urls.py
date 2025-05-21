from django.urls import path, include
from .views import *
urlpatterns = [
    path('create', CreateVehicleView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateVehicleView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteVehicleView.as_view(), name='delete'),
    path('getvehicle/<int:id>/', get_vehicle_by_id_view, name='get'),
    path('list', ListVehicleView.as_view(), name='list'),

]   