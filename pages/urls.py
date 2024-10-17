from django.urls import include, path
from tickets.views import ticket_status
from .views import HomePageView, AboutPageView, home_redirect

urlpatterns = [
    path('', home_redirect, name='home_redirect'),
    path('home/', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('tickets/', include('tickets.urls')),
    path('accounts/', include('allauth.urls')),
]

