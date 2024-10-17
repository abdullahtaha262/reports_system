from django import forms
from .models import Ticket
from django.utils.translation import gettext_lazy as _

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'picture']
        labels = {
            'title': _('Title'),
            'description': _('Description'),
            'picture': _('Upload Picture'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
