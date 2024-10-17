from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ticket
from .forms import TicketForm

def is_customer(user):
    return user.user_type == 'customer'

@login_required
@user_passes_test(is_customer)
def open_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()
            return redirect('ticket_status')
    else:
        form = TicketForm()
    return render(request, 'tickets/open_ticket.html', {'form': form})

@login_required
@user_passes_test(is_customer)
def ticket_status(request):
    tickets = Ticket.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'tickets/ticket_status.html', {'tickets': tickets})

@login_required
@user_passes_test(is_customer)
def ticket_history(request):
    solved_tickets = Ticket.objects.filter(customer=request.user, status='solved').order_by('-updated_at')
    return render(request, 'tickets/ticket_history.html', {'tickets': solved_tickets})
