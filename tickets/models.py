from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('received', _('Received')),
        ('investigating', _('Investigating')),
        ('solved', _('Solved')),
    ]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'customer'}, verbose_name=_('Customer'), related_name='customer_tickets')
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    picture = models.ImageField(upload_to=lambda instance, filename: f'pictures/{instance.customer.username}/{filename}', blank=True, null=True, verbose_name=_('Picture'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received', verbose_name=_('Status'))
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, limit_choices_to={'user_type': 'support'}, null=True, blank=True, verbose_name=_('Assigned To'), related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.title