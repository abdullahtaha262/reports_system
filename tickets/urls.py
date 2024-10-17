from django.urls import path
from . import views

urlpatterns = [
    path('open/', views.open_ticket, name='open_ticket'),
    path('status/', views.ticket_status, name='ticket_status'),
    path('history/', views.ticket_history, name='ticket_history'),
]
