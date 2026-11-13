import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .content import SITE_COPY, SUPPORTED_LANGS
from .forms import ContactForm

logger = logging.getLogger(__name__)


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


def approach_redirect(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)
    return redirect("home:services", lang=lang, permanent=True)


def contact_view(request: HttpRequest, lang: str) -> HttpResponse:
    lang = _validate_lang(lang)

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.language = lang
            lead.save()

            subject = f"Nueva consulta web de {lead.full_name}"
            body = "\n".join(
                (
                    "Se recibió una nueva consulta desde astracore.cl.",
                    "",
                    f"Nombre: {lead.full_name}",
                    f"Correo: {lead.email}",
                    f"Organización: {lead.organization or 'No indicada'}",
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
                logger.exception("Could not email contact inquiry %s", lead.pk)

            messages.success(request, SITE_COPY[lang]["contact"]["success"])
            return redirect(reverse("home:contact", kwargs={"lang": lang}))
    else:
        form = ContactForm()

    return _render_page(
        request,
        lang,
        "home/contact.html",
        {"form": form},
    )
