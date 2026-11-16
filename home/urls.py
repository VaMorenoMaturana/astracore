from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.index_redirect, name="index_redirect"),
    path("<str:lang>/", views.home_view, name="home"),
    path("<str:lang>/about/", views.about_view, name="about"),
    path("<str:lang>/services/", views.services_view, name="services"),
    path("<str:lang>/project-management/", views.project_management_view, name="projects"),
    path("<str:lang>/our-approach/", views.approach_view, name="approach"),
    path("<str:lang>/privacy/", views.privacy_view, name="privacy"),
    path("<str:lang>/terms/", views.terms_view, name="terms"),
    path("<str:lang>/approach/", views.approach_redirect, name="approach_legacy"),
    path("<str:lang>/contact/", views.contact_view, name="contact"),
]
