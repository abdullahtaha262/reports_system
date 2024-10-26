from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Skill(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Skill Name'))
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', _('Customer')),
        ('support', _('Support')),
    ]

    # Adding additional fields to the AbstractUser
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name=_('User Type'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'), blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True, verbose_name=_('Skills'))

    def __str__(self):
        if self.user_type == "customer":
            return f"{self.username} ({self.phone_number})"
        else:
            return f"{self.username} - {self.first_name} - {', '.join([skill.name for skill in self.skills.all()])}"

    def clean(self):
        if self.is_superuser:
            raise ValidationError(_('Admins cannot be customers or supports.'))
