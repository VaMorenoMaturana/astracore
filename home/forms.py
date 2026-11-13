from django import forms

from .models import ContactLead


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactLead
        fields = ["full_name", "email", "organization", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_honeypot(self):
        if self.cleaned_data.get("honeypot"):
            raise forms.ValidationError("Invalid form submission.")
        return ""
