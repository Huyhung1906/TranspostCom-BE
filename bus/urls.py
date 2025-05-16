from django.urls import path, include
from .views import *
urlpatterns = [
    path('create', createbusview.as_view(), name='create'),
    path('update/<int:pk>/', updatebusview.as_view(), name='update'),
    path('delete/<int:pk>/', deletebusview.as_view(), name='delete'),
    path('getbus/<int:id>/', getbusbyidview, name='get'),
    path('list', listbusview.as_view(), name='list'),

]   