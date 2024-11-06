from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tickets.forms import TicketForm
from tickets.models import Ticket, TicketSettings

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
                context['denied_tickets'] = Ticket.objects.filter(
                    customer=user, status='denied'
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

                # Get expected_response_duration from TicketSettings
                settings = TicketSettings.objects.first()
                if settings and settings.expected_response_duration:
                    duration = settings.expected_response_duration
                else:
                    # Set a default duration if settings are not defined
                    duration = timedelta(hours=48)  # Default to 48 hours

                # Calculate expected_response
                ticket.expected_response = timezone.now() + duration

                ticket.save()
                return redirect('home')
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        elif request.user.user_type == 'customer':
            return super().get(request, *args, **kwargs)
        elif request.user.user_type == 'support':
            return redirect('support_dashboard')
        else:
            return redirect('/admin/')

@login_required
def home_redirect(request):
    """Redirect based on user type."""
    if request.user.is_anonymous:
        return redirect('/accounts/login')
    if request.user.user_type == 'customer':
        return redirect('home')
    elif request.user.user_type == 'support':
        return redirect('support_dashboard')
    else:
        return redirect('/admin/')


class SupportDashboardView(TemplateView):
    template_name = "pages/support_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated and user.user_type == 'support':
            # Tickets assigned to the support user, grouped by status
            context['received_tickets'] = Ticket.objects.filter(
                assigned_to=user, status='received'
            ).order_by('-created_at')
            context['investigating_tickets'] = Ticket.objects.filter(
                assigned_to=user, status='investigating'
            ).order_by('-created_at')
            context['solved_tickets'] = Ticket.objects.filter(
                assigned_to=user, status='solved'
            ).order_by('-created_at')
            context['denied_tickets'] = Ticket.objects.filter(
                assigned_to=user, status='denied'
            ).order_by('-created_at')
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        elif request.user.user_type == 'support':
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/')

@login_required
def support_dashboard(request):
    if request.user.user_type == 'support':
        return redirect('support_dashboard')
    else:
        return redirect('/')

@login_required
def update_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, assigned_to=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        response_message = request.POST.get('response_message', '').strip()
        ticket.status = new_status
        ticket.response_message = response_message
        ticket.save()
        return redirect('support_dashboard')

    return redirect('support_dashboard')


class AboutPageView(TemplateView):
    template_name = "pages/about.html"
