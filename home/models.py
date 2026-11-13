from django.db import models


class ContactLead(models.Model):
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    organization = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    language = models.CharField(max_length=2, default="es")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"
