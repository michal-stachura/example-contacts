import pytest

from django.urls import resolve, reverse
from django.conf import settings

from example_contacts.issues.models import ContactForm
from example_contacts.issues.tests.fixtures import contact_form_fixture
from example_contacts.issues.views import (
    contact_form,
    thankyou_page,
    contact_form_list,
    contact_form_detail,
    update_contact_form_status,
    ContactFormViewSet
)

test_contact_form = contact_form_fixture
pytestmark = pytest.mark.django_db

class TestContactFormUrls:

    def test_contact_form(self) -> None:
        "GET, POST"
        assert (
            reverse("issues:contact_form") == f"/contact/"
        )
        assert (
            resolve(f"/contact/").view_name == "issues:contact_form"
        )
        assert (
            resolve(f"/contact/").func == contact_form
        )
    
    def test_thankyou_page(self) -> None:
        "GET"
        assert (
            reverse("issues:thank_you") == f"/contact/confirm/"
        )
        assert (
            resolve(f"/contact/confirm/").view_name == "issues:thank_you"
        )
        assert (
            resolve(f"/contact/confirm/").func == thankyou_page
        )
    
    def test_contact_form_list(self) -> None:
        "GET"
        assert (
            reverse("issues:contact_form_list") == f"/contact/issues/"
        )
        assert (
            resolve(f"/contact/issues/").view_name == "issues:contact_form_list"
        )
        assert (
            resolve(f"/contact/issues/").func == contact_form_list
        )
    
    def test_contact_form_details(self, test_contact_form: ContactForm) -> None:
        "GET"
        assert (
            reverse(
                "issues:contact_form_detail",
                kwargs={"uuid": str(test_contact_form.id)}
            ) == f"/contact/issues/{str(test_contact_form.id)}/"
        )
        assert (
            resolve(f"/contact/issues/{str(test_contact_form.id)}/").view_name == "issues:contact_form_detail"
        )
        assert (
            resolve(f"/contact/issues/{str(test_contact_form.id)}/").func == contact_form_detail
        )
    
    def test_update_contact_form_status(self, test_contact_form: ContactForm) -> None:
        "POST"
        assert (
            reverse(
                "issues:update_contact_form_status",
                kwargs={"uuid": str(test_contact_form.id)}
            ) == f"/contact/issues/{str(test_contact_form.id)}/status-change/"
        )
        assert (
            resolve(f"/contact/issues/{str(test_contact_form.id)}/status-change/").view_name == "issues:update_contact_form_status"
        )
        assert (
            resolve(f"/contact/issues/{str(test_contact_form.id)}/status-change/").func == update_contact_form_status
        )

class TestContactFormApiUrls:
    def test_list(self) -> None:
        "GET, POST"
        assert (
            reverse("api-issues:contactform-list") == f"/api/{settings.API_VERSION}/issues/"
        )
        assert (
            resolve(f"/api/{settings.API_VERSION}/issues/").view_name == "api-issues:contactform-list"
        )
        assert (
            resolve(f"/api/{settings.API_VERSION}/issues/").func.cls == ContactFormViewSet
        )

    def test_detail(self, test_contact_form: ContactForm) -> None:
        "GET"
        assert (
            reverse(
                "api-issues:contactform-detail",
                kwargs={"id": str(test_contact_form.id)}
            ) == f"/api/{settings.API_VERSION}/issues/{str(test_contact_form.id)}/"
        )
        assert (
            resolve(f"/api/{settings.API_VERSION}/issues/{str(test_contact_form.id)}/").view_name == "api-issues:contactform-detail"
        )
        assert (
            resolve(f"/api/{settings.API_VERSION}/issues/{str(test_contact_form.id)}/").func.cls == ContactFormViewSet
        )

    def test_action_update_status(self, test_contact_form: ContactForm) -> None:
        "PATCH"
        assert (
            reverse(
                "api-issues:contactform-status-change",
                kwargs={"id": str(test_contact_form.id)}
            ) == f"/api/{settings.API_VERSION}/issues/{str(test_contact_form.id)}/status-change/"
        )
        assert (
            resolve(f"/api/{settings.API_VERSION}/issues/{str(test_contact_form.id)}/status-change/").view_name == "api-issues:contactform-status-change"
        )
        assert (
            resolve(f"/api/{settings.API_VERSION}/issues/{str(test_contact_form.id)}/status-change/").func.cls == ContactFormViewSet
        )
