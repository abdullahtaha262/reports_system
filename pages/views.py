from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from tickets.forms import TicketForm
from tickets.models import Ticket

class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            if user.user_type == 'customer':
                context['ticket_form'] = TicketForm()
                context['tickets'] = Ticket.objects.filter(customer=user).order_by('-created_at')
                context['solved_tickets'] = Ticket.objects.filter(
                    customer=user, status='solved'
                ).order_by('-updated_at')
                context['received_tickets'] = Ticket.objects.filter(
                    customer=user, status='received'
                ).order_by('-updated_at')
                context['investigating_tickets'] = Ticket.objects.filter(
                    customer=user, status='investigating'
                ).order_by('-updated_at')
            return context
            

    def post(self, request, *args, **kwargs):
        if request.user.user_type == 'customer':
            form = TicketForm(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.customer = request.user
                ticket.save()
                return redirect('home')
        return self.get(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        elif request.user.user_type == 'customer':
            return super().get(request, *args, **kwargs)
        elif request.user.user_type == 'support':
            return redirect('support_dashboard')  # To be implemented later
        else:
            return redirect('/admin/')  # Admin users redirected to admin panel
        
    
    

@login_required
def home_redirect(request):
    """Redirect based on user type."""
    
    if request.user.user_type == 'customer':
        return redirect('home')
    elif request.user.user_type == 'support':
        return redirect('support_dashboard')  # To be implemented later
    else:
        return redirect('/admin/')  # Admin users redirected to admin panel

    
    


class AboutPageView(TemplateView):
    template_name = "pages/about.html"
