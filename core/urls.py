from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from home.sitemaps import PublicPagesSitemap

sitemaps = {"public": PublicPagesSitemap()}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="home/robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("home.urls")),
]
