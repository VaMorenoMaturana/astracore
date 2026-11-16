from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from home.sitemaps import PublicPagesSitemap

sitemaps = {"public": PublicPagesSitemap()}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("home.urls")),
]
