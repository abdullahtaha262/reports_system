from django.contrib import admin
from .models import Ticket, TicketSettings
from django import forms
from django.utils.translation import gettext_lazy as _, ngettext
from datetime import timedelta


class TicketSettingsAdminForm(forms.ModelForm):
    expected_response_duration_hours = forms.FloatField(
        label=_('Expected Response Duration (in hours)'),
        required=False,
        help_text=_('Enter the expected response duration in hours.')
    )

    class Meta:
        model = TicketSettings
        fields = []  # Exclude all fields from automatic processing

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the hours field from the existing duration
        if self.instance and self.instance.expected_response_duration:
            total_seconds = self.instance.expected_response_duration.total_seconds()
            hours = total_seconds / 3600  # Convert seconds to hours
            self.fields['expected_response_duration_hours'].initial = hours
        else:
            self.fields['expected_response_duration_hours'].initial = None

    def save(self, commit=True):
        # Get the hours input from the form
        hours = self.cleaned_data.get('expected_response_duration_hours')

        if hours is not None:
            # Convert hours to timedelta
            self.instance.expected_response_duration = timedelta(hours=hours)
        else:
            self.instance.expected_response_duration = None

        return super().save(commit=commit)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'status', 'response_message', 'assigned_to', 'created_at', 'updated_at')
    search_fields = ('title', 'customer__user__username', 'assigned_to__user__username', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    readonly_fields = ('title', 'description', 'customer', 'status', 'response_message', 'picture', 'created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-created_at',)
    

@admin.register(TicketSettings)
class TicketSettingsAdmin(admin.ModelAdmin):
    form = TicketSettingsAdminForm
    list_display = ('expected_response_duration_display',)

    def expected_response_duration_display(self, obj):
        if obj.expected_response_duration:
            total_seconds = int(obj.expected_response_duration.total_seconds())
            days, remainder = divmod(total_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            parts = []
            if days:
                day_text = _("%d days") % days
                parts.append(day_text)
            if hours:
                hour_text = _("%d hours") % hours
                parts.append(hour_text)
            if minutes:
                minute_text = _("%d minutes") % minutes
                parts.append(minute_text)
            return ", ".join(parts)
        else:
            return _("Not set")

    expected_response_duration_display.short_description = _('Expected Response Duration')

