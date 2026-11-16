import re
from xml.etree import ElementTree
from urllib.parse import urlparse

from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .models import ContactLead


class InstitutionalContentTests(SimpleTestCase):
    def test_robots_txt_allows_crawling_and_links_to_sitemap(self):
        response = self.client.get(reverse("robots"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
        self.assertEqual(
            response.content.decode(),
            "User-agent: *\nAllow: /\n\nSitemap: https://www.astracore.cl/sitemap.xml",
        )

    def test_sitemap_lists_each_public_page_in_all_languages(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        root = ElementTree.fromstring(response.content)
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locations = [
            element.text
            for element in root.findall(f"{namespace}url/{namespace}loc")
        ]
        self.assertEqual(len(locations), 24)
        self.assertTrue(all(location.startswith("https://www.astracore.cl/") for location in locations))
        paths = {urlparse(location).path for location in locations}
        for language in ("es", "en", "zh"):
            for page in ("home", "about", "services", "projects", "approach", "contact", "privacy", "terms"):
                with self.subTest(language=language, page=page):
                    self.assertIn(
                        reverse(f"home:{page}", kwargs={"lang": language}),
                        paths,
                    )

    def test_public_pages_render_in_both_languages(self):
        for language in ("es", "en", "zh"):
            for name in ("home", "about", "services", "projects", "approach", "contact", "privacy", "terms"):
                with self.subTest(language=language, page=name):
                    response = self.client.get(reverse(f"home:{name}", kwargs={"lang": language}))
                    self.assertEqual(response.status_code, 200)
                    html_language = "zh-Hans" if language == "zh" else language
                    self.assertContains(response, f'<html lang="{html_language}">')
                    if language == "zh":
                        self.assertContains(response, "中文")
                    self.assertNotContains(response, "CEDAR", status_code=200)
                    self.assertNotContains(response, "Wellness Group", status_code=200)
                    self.assertNotContains(response, "holding", status_code=200)

    def test_localized_pages_have_canonical_and_hreflang_links(self):
        hreflang_codes = {"es": "es", "en": "en", "zh": "zh-Hans"}
        page_names = ("home", "about", "services", "projects", "approach", "contact", "privacy", "terms")
        for page_name in page_names:
            urls = {
                language: f"https://www.astracore.cl{reverse(f'home:{page_name}', kwargs={'lang': language})}"
                for language in hreflang_codes
            }
            for language, code in hreflang_codes.items():
                with self.subTest(page=page_name, language=language):
                    response = self.client.get(reverse(f"home:{page_name}", kwargs={"lang": language}))
                    self.assertContains(response, f'<link rel="canonical" href="{urls[language]}">')
                    for alternate_language, alternate_code in hreflang_codes.items():
                        self.assertContains(
                            response,
                            f'<link rel="alternate" hreflang="{alternate_code}" href="{urls[alternate_language]}">',
                        )
                    self.assertContains(
                        response,
                        f'<link rel="alternate" hreflang="x-default" href="{urls["es"]}">',
                    )

    def test_home_describes_astracore_as_a_company(self):
        response = self.client.get(reverse("home:home", kwargs={"lang": "es"}))
        self.assertContains(
            response,
            "Astracore Group es una empresa chilena que integra consultoría especializada, desarrollo de negocios y dirección de proyectos. Articulamos capacidades jurídicas, técnicas, económicas e institucionales para transformar oportunidades en iniciativas concretas.",
        )
        self.assertContains(
            response,
            "ASTRACORE GROUP · CONSULTORÍA ESPECIALIZADA · DESARROLLO DE NEGOCIOS · DIRECCIÓN DE PROYECTOS",
        )

        for language in ("es", "en"):
            for page in ("about", "services"):
                with self.subTest(language=language, page=page):
                    response = self.client.get(reverse(f"home:{page}", kwargs={"lang": language}))
                    self.assertNotContains(response, "plataforma")
                    self.assertNotContains(response, "business platform")

    def test_services_have_four_expandable_areas(self):
        response = self.client.get(reverse("home:services", kwargs={"lang": "es"}))
        self.assertContains(response, 'class="service-details"', count=4)
        self.assertContains(response, "Gestión y gobernanza de recursos hídricos.")
        self.assertContains(response, "<title>Servicios | Astracore Group</title>")
        for interest in (
            "environment",
            "project_structuring",
            "logistics_territorial",
            "real_estate_investment",
        ):
            with self.subTest(interest=interest):
                self.assertContains(response, f"?interest={interest}")

    def test_home_area_links_prefill_contact_interest(self):
        response = self.client.get(reverse("home:home", kwargs={"lang": "es"}))
        for interest in (
            "environment",
            "project_structuring",
            "logistics_territorial",
            "real_estate_investment",
        ):
            with self.subTest(interest=interest):
                self.assertContains(response, f"?interest={interest}")

        response = self.client.get(
            reverse("home:contact", kwargs={"lang": "es"}),
            {"interest": "project_management"},
        )
        self.assertEqual(response.context["form"]["interest"].value(), "project_management")

    def test_project_management_has_six_stages(self):
        for language in ("es", "en", "zh"):
            with self.subTest(language=language):
                response = self.client.get(reverse("home:projects", kwargs={"lang": language}))
                self.assertContains(response, 'class="service-capability"', count=6)
                self.assertContains(response, 'class="stage-result"', count=6)
                self.assertContains(response, reverse("home:projects", kwargs={"lang": "en"}))
                self.assertContains(response, reverse("home:projects", kwargs={"lang": "es"}))
                self.assertContains(response, reverse("home:projects", kwargs={"lang": "zh"}))

    def test_chinese_contact_form_uses_simplified_chinese_choices(self):
        response = self.client.get(reverse("home:contact", kwargs={"lang": "zh"}))
        self.assertContains(response, "请选择感兴趣的领域")
        self.assertContains(response, "环境与可持续发展")
        self.assertContains(response, "手机号码（选填）")
        choices = response.context["form"].fields["interest"].choices
        self.assertEqual([value for value, _ in choices[1:]], [
            "environment",
            "project_structuring",
            "logistics_territorial",
            "real_estate_investment",
            "project_management",
            "business_development",
            "other",
        ])

        response = self.client.post(reverse("home:contact", kwargs={"lang": "zh"}), {})
        self.assertContains(response, "此项为必填项。")
        self.assertContains(response, "请先勾选并同意隐私政策。")
        self.assertNotContains(response, "Este campo es obligatorio.")

    def test_legacy_services_url_redirects(self):
        response = self.client.get(reverse("home:approach_legacy", kwargs={"lang": "es"}))
        self.assertRedirects(response, reverse("home:services", kwargs={"lang": "es"}), status_code=301)

    def test_legal_pages_are_linked_from_the_footer(self):
        response = self.client.get(reverse("home:home", kwargs={"lang": "es"}))
        self.assertContains(response, reverse("home:privacy", kwargs={"lang": "es"}))
        self.assertContains(response, reverse("home:terms", kwargs={"lang": "es"}))

    def test_privacy_policy_is_linked_from_required_consent(self):
        response = self.client.get(reverse("home:contact", kwargs={"lang": "es"}))
        self.assertContains(response, reverse("home:privacy", kwargs={"lang": "es"}))
        self.assertContains(response, 'id="id_privacy_consent"')

    def test_interest_selector_has_styled_wrapper(self):
        response = self.client.get(reverse("home:contact", kwargs={"lang": "es"}))
        self.assertContains(response, 'class="interest-select-wrap"')
        self.assertContains(response, 'id="id_interest"')


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_EMAIL="contacto@example.com",
    DEFAULT_FROM_EMAIL="sitio@example.com",
)
class ContactWorkflowTests(TestCase):
    def test_inquiry_is_saved_and_notified(self):
        response = self.client.post(
            reverse("home:contact", kwargs={"lang": "es"}),
            {
                "full_name": "Persona de prueba",
                "email": "consulta@example.com",
                "phone": "+56 9 1234 5678",
                "organization": "Organización de prueba",
                "interest": "environment",
                "message": "Consulta de prueba",
                "privacy_consent": "on",
            },
        )
        self.assertRedirects(response, reverse("home:contact", kwargs={"lang": "es"}))
        self.assertEqual(ContactLead.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)
        lead = ContactLead.objects.get()
        self.assertRegex(lead.consultation_code, r"^\d{10}$")
        self.assertEqual(lead.phone, "+56 9 1234 5678")
        self.assertEqual(lead.interest, "environment")
        self.assertTrue(lead.privacy_consent)
        self.assertIn(lead.consultation_code, mail.outbox[0].subject)
        self.assertIn(lead.consultation_code, mail.outbox[0].body)
        self.assertIn(lead.phone, mail.outbox[0].body)
        self.assertIn("Área de interés: Medio ambiente y sostenibilidad", mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, ["contacto@example.com"])
        self.assertEqual(mail.outbox[0].reply_to, ["consulta@example.com"])
        self.assertEqual(mail.outbox[1].to, ["consulta@example.com"])
        self.assertEqual(mail.outbox[1].reply_to, ["contacto@example.com"])
        self.assertIn(lead.consultation_code, mail.outbox[1].body)

    def test_chinese_inquiry_gets_a_chinese_confirmation(self):
        response = self.client.post(
            reverse("home:contact", kwargs={"lang": "zh"}),
            {
                "full_name": "测试联系人",
                "email": "consulta@example.com",
                "organization": "测试机构",
                "interest": "environment",
                "message": "咨询项目合作",
                "privacy_consent": "on",
            },
        )
        self.assertRedirects(response, reverse("home:contact", kwargs={"lang": "zh"}))
        lead = ContactLead.objects.get()
        self.assertEqual(lead.language, "zh")
        self.assertIn("我们已收到您的咨询", mail.outbox[1].subject)
        self.assertIn("咨询编号", mail.outbox[1].body)

    def test_each_inquiry_gets_a_different_code(self):
        payload = {
            "full_name": "Persona de prueba",
            "email": "consulta@example.com",
            "phone": "+56 9 1234 5678",
            "organization": "Organización de prueba",
            "interest": "environment",
            "message": "Consulta de prueba",
            "privacy_consent": "on",
        }
        for _ in range(2):
            response = self.client.post(reverse("home:contact", kwargs={"lang": "es"}), payload)
            self.assertEqual(response.status_code, 302)

        codes = list(ContactLead.objects.values_list("consultation_code", flat=True))
        self.assertEqual(len(set(codes)), 2)

    def test_phone_is_optional_and_interest_and_privacy_consent_are_required(self):
        base_payload = {
            "full_name": "Persona de prueba",
            "email": "consulta@example.com",
            "phone": "",
            "organization": "Organización de prueba",
            "interest": "environment",
            "message": "Consulta de prueba",
            "privacy_consent": "on",
        }
        response = self.client.post(reverse("home:contact", kwargs={"lang": "es"}), base_payload)
        self.assertRedirects(response, reverse("home:contact", kwargs={"lang": "es"}))
        lead = ContactLead.objects.get()
        self.assertEqual(lead.phone, "")
        self.assertEqual(lead.interest, "environment")

        for field in ("organization", "interest", "privacy_consent"):
            with self.subTest(field=field):
                payload = base_payload.copy()
                payload.pop(field)
                response = self.client.post(reverse("home:contact", kwargs={"lang": "es"}), payload)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(ContactLead.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)