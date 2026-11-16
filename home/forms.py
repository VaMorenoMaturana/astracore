from django import forms

from .models import ContactLead


INTEREST_CHOICES = {
    "es": [
        ("environment", "Medio ambiente y sostenibilidad"),
        ("project_structuring", "Estructuración y evaluación de proyectos"),
        ("logistics_territorial", "Logística, desarrollo empresarial y territorial"),
        ("real_estate_investment", "Desarrollo inmobiliario y proyectos de inversión"),
        ("project_management", "Gestión de proyectos"),
        ("business_development", "Desarrollo de negocios y alianzas"),
        ("other", "Otro o necesito orientación"),
    ],
    "en": [
        ("environment", "Environment and sustainability"),
        ("project_structuring", "Project structuring and assessment"),
        ("logistics_territorial", "Logistics, business and territorial development"),
        ("real_estate_investment", "Real estate and investment project development"),
        ("project_management", "Project management"),
        ("business_development", "Business development and partnerships"),
        ("other", "Other or I need guidance"),
    ],
}


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    phone = forms.CharField(
        max_length=32,
        required=False,
        widget=forms.TextInput(
            attrs={"type": "tel", "autocomplete": "tel", "inputmode": "tel"}
        ),
    )
    organization = forms.CharField(max_length=180, required=True)
    interest = forms.ChoiceField(required=True)
    privacy_consent = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={"aria-describedby": "privacy-note"}),
    )

    class Meta:
        model = ContactLead
        fields = ["full_name", "email", "phone", "organization", "interest", "message", "privacy_consent"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, language="es", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["interest"].choices = [
            ("", INTEREST_PLACEHOLDERS.get(language, INTEREST_PLACEHOLDERS["es"])),
            *INTEREST_CHOICES.get(language, INTEREST_CHOICES["es"]),
        ]

    def clean_honeypot(self):
        if self.cleaned_data.get("honeypot"):
            raise forms.ValidationError("Invalid form submission.")
        return ""


INTEREST_PLACEHOLDERS = {
    "es": "Seleccione un área de interés",
    "en": "Select an area of interest",
}
