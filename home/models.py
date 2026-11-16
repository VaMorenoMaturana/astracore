from django.db import models


class ContactLead(models.Model):
    consultation_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True, default="")
    organization = models.CharField(max_length=180, blank=True)
    interest = models.CharField(max_length=64, blank=True, default="")
    message = models.TextField()
    privacy_consent = models.BooleanField(default=False)
    language = models.CharField(max_length=2, default="es")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
