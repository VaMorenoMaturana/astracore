from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content import SUPPORTED_LANGS


class PublicPagesSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.7

    def get_domain(self, site=None):
        return "www.astracore.cl"

    page_names = (
        "home",
        "about",
        "services",
        "projects",
        "approach",
        "contact",
        "privacy",
        "terms",
    )

    def items(self):
        return [
            (language, page_name)
            for language in sorted(SUPPORTED_LANGS)
            for page_name in self.page_names
        ]

    def location(self, item):
        language, page_name = item
        return reverse(f"home:{page_name}", kwargs={"lang": language})