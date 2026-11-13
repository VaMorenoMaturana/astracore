from .content import NAV_ITEMS, SITE_COPY


def brand_context(request):
    resolver_match = request.resolver_match
    lang = resolver_match.kwargs.get("lang", "es") if resolver_match else "es"
    lang = lang if lang in SITE_COPY else "es"

    return {
        "brand_name": "Astracore Group",
        "brand_statement": SITE_COPY[lang]["brand_statement"],
        "supported_langs": ("es", "en"),
        "nav_items": NAV_ITEMS,
        "copy": SITE_COPY[lang],
        "current_lang": lang,
        "current_view": resolver_match.url_name if resolver_match else "home",
    }
