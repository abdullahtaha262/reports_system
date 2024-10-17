from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type', 'phone_number', 'skills']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        skills = cleaned_data.get('skills')

        # Validate that customers don't have skills
        if user_type == 'customer' and skills:
            raise ValidationError(_('Customers cannot have skills.'))

        # Validate that support users must have at least one skill
        if user_type == 'support' and not skills:
            raise ValidationError(_('Support must have at least one skill.'))

        return cleaned_data
