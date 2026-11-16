from django.urls import reverse

from .content import NAV_ITEMS, SITE_COPY
from .legal_content import LEGAL_COPY

CANONICAL_ORIGIN = "https://www.astracore.cl"
HREFLANG_CODES = {"es": "es", "en": "en", "zh": "zh-Hans"}
LOCALIZED_PAGE_NAMES = {
    "home",
    "about",
    "services",
    "projects",
    "approach",
    "contact",
    "privacy",
    "terms",
}


def brand_context(request):
    resolver_match = request.resolver_match
    lang = resolver_match.kwargs.get("lang", "es") if resolver_match else "es"
    lang = lang if lang in SITE_COPY else "es"
    current_view = resolver_match.url_name if resolver_match else "home"
    copy = SITE_COPY[lang]
    copy.update(LEGAL_COPY[lang])
    page_copy = copy.get("project_management" if current_view == "projects" else current_view, {})
    localized_urls = {}
    if current_view in LOCALIZED_PAGE_NAMES:
        localized_urls = {
            language: f"{CANONICAL_ORIGIN}{reverse(f'home:{current_view}', kwargs={'lang': language})}"
            for language in SITE_COPY
        }

    return {
        "brand_name": "Astracore Group",
        "brand_statement": copy["brand_statement"],
        "supported_langs": ("es", "en", "zh"),
        "nav_items": NAV_ITEMS,
        "copy": copy,
        "current_lang": lang,
        "current_view": current_view,
        "seo_title": page_copy.get("seo_title", copy["site_title"]),
        "seo_description": page_copy.get("seo_description", copy["meta_description"]),
        "canonical_url": localized_urls.get(lang, ""),
        "hreflang_urls": [
            {"code": HREFLANG_CODES[language], "url": url}
            for language, url in localized_urls.items()
        ],
        "x_default_url": localized_urls.get("es", ""),
    }
