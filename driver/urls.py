from django.urls import path, include
from .views import *
urlpatterns = [
    path('create/', CreateDriverView.as_view(), name='create'),
    path('update/<int:pk>/', updatedriverview.as_view(), name='update'),
    path('delete/<int:pk>/', deletedriverview.as_view(), name='delete'),
    path('getdriver/<int:id>/', getdriverbyidview, name='get'),
    path('list', listdriverview.as_view(), name='list'),

]