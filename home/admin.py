from django.contrib import admin

from .forms import INTEREST_CHOICES
from .models import ContactLead


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("consultation_code", "full_name", "email", "phone", "organization", "interest_display", "privacy_consent", "language", "created_at")
    search_fields = ("consultation_code", "full_name", "email", "phone", "organization", "interest")
    list_filter = ("language", "created_at")

    @admin.display(description="Área de interés")
    def interest_display(self, obj):
        return dict(INTEREST_CHOICES.get(obj.language, INTEREST_CHOICES["es"])).get(obj.interest, obj.interest)
