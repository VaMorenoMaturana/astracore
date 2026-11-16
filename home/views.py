import logging
import secrets

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .content import SITE_COPY, SUPPORTED_LANGS
from .forms import ContactForm, INTEREST_CHOICES
from .models import ContactLead

logger = logging.getLogger(__name__)


def _generate_consultation_code() -> str:
    for _ in range(20):
        code = str(secrets.randbelow(9_000_000_000) + 1_000_000_000)
        if not ContactLead.objects.filter(consultation_code=code).exists():
            return code
    raise RuntimeError("Could not generate a unique consultation code.")


def _validate_lang(lang: str) -> str:
    if lang not in SUPPORTED_LANGS:
        raise Http404("Language not supported")
    return lang


def _render_page(request: HttpRequest, lang: str, template_name: str, extra_context: dict | None = None) -> HttpResponse:
    context = {"copy": SITE_COPY[lang], "current_lang": lang}
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)


def index_redirect(request: HttpRequest) -> HttpResponse:
    return redirect("home:home", lang="es")


def home_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/index.html")


def about_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/about.html")


def services_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/services.html")


def project_management_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/project_management.html")


def approach_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/approach.html")


def privacy_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/privacy.html")


def terms_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return _render_page(request, lang, "home/terms.html")


def approach_redirect(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return redirect("home:services", lang=lang, permanent=True)


def contact_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)

    if request.method == "POST":
        form = ContactForm(request.POST, language=lang)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.language = lang
            lead.consultation_code = _generate_consultation_code()
            lead.save()
            interest_label = dict(INTEREST_CHOICES[lang]).get(lead.interest, lead.interest)

            subject = f"Nueva consulta web [{lead.consultation_code}] de {lead.full_name}"
            body = "\n".join(
                (
                    "Se recibió una nueva consulta desde astracore.cl.",
                    "",
                    f"Código de consulta: {lead.consultation_code}",
                    f"Nombre: {lead.full_name}",
                        f"Correo: {lead.email}",
                        f"Teléfono: {lead.phone or 'No indicado'}",
                    f"Organización: {lead.organization or 'No indicada'}",
                    f"Área de interés: {interest_label}",
                    f"Idioma: {lead.language.upper()}",
                    "",
                    "Mensaje:",
                    lead.message,
                )
            )
            try:
                email = EmailMessage(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_EMAIL],
                    reply_to=[lead.email],
                )
                email.send(fail_silently=False)
            except Exception:
                logger.exception("Could not send internal notification for inquiry %s", lead.pk)

            contact_copy = SITE_COPY[lang]["contact"]
            confirmation_body = "\n\n".join(
                (
                    contact_copy["confirmation_message"],
                    f"{contact_copy['confirmation_code_label']}: {lead.consultation_code}",
                )
            )
            try:
                confirmation = EmailMessage(
                    contact_copy["confirmation_subject"],
                    confirmation_body,
                    settings.DEFAULT_FROM_EMAIL,
                    to=[lead.email],
                    reply_to=[settings.CONTACT_EMAIL],
                )
                confirmation.send(fail_silently=False)
            except Exception:
                logger.exception("Could not send confirmation for contact inquiry %s", lead.pk)

            messages.success(
                request,
                SITE_COPY[lang]["contact"]["success"].format(code=lead.consultation_code),
            )
            return redirect(reverse("home:contact", kwargs={"lang": lang}))
    else:
        form = ContactForm(
            initial={"interest": request.GET.get("interest", "")},
            language=lang,
        )

    return _render_page(
        request,
        lang,
        "home/contact.html",
        {"form": form},
    )
