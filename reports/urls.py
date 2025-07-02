from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.ticket_sales_and_revenue_by_month, name='summary_report'),
    path('tickets-online/', views.online_ticket_sales_by_month, name='online_ticket_sales_by_month'),
    path('top/vehicles/', views.top_vehicles, name='top_vehicles'),
    path('top/driver/', views.top_drivers, name='top_drivers'),
    path('top/vehicles-by-month/', views.top_vehicles_by_month, name='top_vehicles_by_month'),
    path('top/drivers-by-month/', views.top_drivers_by_month, name='top_drivers_by_month'),
]
