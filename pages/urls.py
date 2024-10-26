from django.urls import include, path
from tickets.views import ticket_status
from .views import HomePageView, AboutPageView, SupportDashboardView, home_redirect, update_ticket_status

urlpatterns = [
    path('', home_redirect, name='home_redirect'),
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('tickets/', include('tickets.urls')),
    path('support_dashboard/', SupportDashboardView.as_view(), name='support_dashboard'),
    path('update_ticket_status/<int:ticket_id>/', update_ticket_status, name='update_ticket_status'),
    path('accounts/', include('allauth.urls')),
]

