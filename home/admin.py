from django.contrib import admin

from .models import ContactLead


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "organization", "language", "created_at")
    search_fields = ("full_name", "email", "organization")
    list_filter = ("language", "created_at")
