from .content import NAV_ITEMS, SITE_COPY
from .legal_content import LEGAL_COPY


def brand_context(request):
    resolver_match = request.resolver_match
    lang = resolver_match.kwargs.get("lang", "es") if resolver_match else "es"
    lang = lang if lang in SITE_COPY else "es"
    current_view = resolver_match.url_name if resolver_match else "home"
    copy = SITE_COPY[lang]
    copy.update(LEGAL_COPY[lang])
    page_copy = copy.get("project_management" if current_view == "projects" else current_view, {})

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
    }
