from django.urls import path, include
from .views import *
urlpatterns = [
    path('created/', CreateDriverView.as_view(), name='created'),


]