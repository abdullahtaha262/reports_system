from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'status', 'response_message', 'assigned_to', 'created_at', 'updated_at')
    search_fields = ('title', 'customer__user__username', 'assigned_to__user__username', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    readonly_fields = ('title', 'description', 'customer', 'status', 'response_message', 'picture', 'created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-created_at',)