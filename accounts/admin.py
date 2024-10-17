from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill
from .forms import CustomUserForm
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Use the custom form for the UserProfile model
    form = CustomUserForm

    # Add our custom fields to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'phone_number', 'skills')}),
    )

    # List display configuration
    list_display = ('username', 'email', 'user_type', 'phone_number', 'get_skills', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'user_type')
    list_filter = ('user_type', 'is_staff')
    list_per_page = 20

    def get_skills(self, obj):
        """Helper method to display skills in a comma-separated format."""
        return ", ".join([skill.name for skill in obj.skills.all()])
    get_skills.short_description = _('Skills')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20
