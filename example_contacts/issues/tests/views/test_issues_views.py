import pytest
from bs4 import BeautifulSoup

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from factory import build

from example_contacts.issues.models import ContactForm
from example_contacts.issues.tests.factories import ContactFormFactory
from example_contacts.issues.tests.fixtures import contact_form_fixture
from example_contacts.users.tests.fixtures import admin_fixture
from example_contacts.users.models import User
from example_contacts.issues.serializers import ContactFormDetailSerializer

test_contact_form = contact_form_fixture
admin_user = admin_fixture
pytestmark = pytest.mark.django_db


class TestContactFormCommonViews:
    
    def test_contact_form_and_confirm_page(self) -> None:
        url = reverse("issues:contact_form")
        response = APIClient().get(url)

        assert response.status_code == 200
        
        soup = BeautifulSoup(response.content, "html.parser")
        assert str(soup.find("h1")) == "<h1>Please Leave message here</h1>"
        assert soup.find("form", {"method": "POST", "action": url}) is not None

        valid_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )

        response = APIClient().post(url, data=valid_data)
        assert response.status_code == 302
        assert response.url == reverse("issues:thank_you")
        assert ContactForm.objects.all().count() == 1

        response = APIClient().get(response.url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, "html.parser")
        assert str(soup.find("h1")) == "<h1>Thank you for the message</h1>"

    def test_contact_form_invalid_data(self) -> None:
        url = reverse("issues:contact_form")

        invalid_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )
        invalid_data["name"] = "ABC"

        response = APIClient().post(url, data=invalid_data)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, "html.parser")
        assert str(soup.find("p", {"id": "error_1_id_name"})) == """<p class="invalid-feedback" id="error_1_id_name"><strong>Ensure this value has at least 5 characters (it has 3).</strong></p>"""
        assert ContactForm.objects.all().count() == 0

    def test_contact_form_list(self, admin_user: User) -> None:
        url = reverse("issues:contact_form_list")
        client = APIClient()
        admin = admin_user
        admin.set_password("abc123")
        admin.save()

        response = client.get(url)
        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/contact/issues/"
        client.login(
            username=admin.username,
            password="abc123"
        )
        response = client.get(url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, "html.parser")
        assert str(soup.find("h1")) == "<h1>Issues list</h1>"

    def test_contact_form_details(self, admin_user: User, test_contact_form: ContactForm) -> None:
        url = reverse("issues:contact_form_detail", kwargs={"uuid": str(test_contact_form.id)})
        client = APIClient()
        admin = admin_user
        admin.set_password("abc123")
        admin.save()

        response = client.get(url)
        assert response.status_code == 302
        assert response.url == f"/accounts/login/?next=/contact/issues/{str(test_contact_form.id)}/"
        client.login(
            username=admin.username,
            password="abc123"
        )
        response = client.get(url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, "html.parser")
        assert str(soup.find("h1")) == "<h1>Issue detail</h1>"


class TestContactFormViewSet:

    def setup_class(self):
        self.endpoint = reverse("api-issues:contactform-list")
        self.client = APIClient()

    def test_list(self, admin_user: User) -> None:
        ContactFormFactory.create_batch(settings.PAGE_SIZE + 2)

        response = self.client.get(self.endpoint)
        assert response.status_code == 403

        self.client.force_authenticate(
            user=admin_user
        )
        response = self.client.get(self.endpoint)
        assert response.status_code == 200
        assert len(response.data["results"]) == settings.PAGE_SIZE
        assert response.data["next"] is not None
    
    def test_create(self) -> None:
        valid_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )

        self.client.force_authenticate(
            user = None
        )
        response = self.client.post(self.endpoint, data=valid_data)

        try:
            contact_form_object = ContactForm.objects.get(id=response.data["id"])
            serializer = ContactFormDetailSerializer(contact_form_object)

        except ContactForm.DoesNotExist:
            contact_form_object = None
            serializer = None

        assert contact_form_object is not None
        assert serializer is not None

        assert response.status_code == 201
        assert ContactForm.objects.all().count() == 1
        assert response.data == serializer.data

    def test_create_invalid_data(self) -> None:
        invalid_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )
        invalid_data["email"] = "not_valid_email_address"
        respoonse = self.client.post(self.endpoint, data=invalid_data)
        
        assert respoonse.status_code == 400
        assert ContactForm.objects.all().count() == 0

    def test_retrieve(self, admin_user: User, test_contact_form: ContactForm) -> None:
        url = f"{self.endpoint}{str(test_contact_form.id)}/"
        self.client.force_authenticate(
            user = None
        )
        response = self.client.get(url)
        assert response.status_code == 403

        self.client.force_authenticate(
            user = admin_user
        )

        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["id"] == str(test_contact_form.id)

    def test_update_status(self, admin_user: User, test_contact_form: ContactForm) -> None:
        url = f"{self.endpoint}{str(test_contact_form.id)}/status-change/"
        self.client.force_authenticate(
            user = None
        )
        data = {"status": "in-progress"}
        response = self.client.patch(url, data=data)
        assert response.status_code == 403

        self.client.force_authenticate(
            user=admin_user
        )
        response = self.client.patch(url, data=data)
        assert response.status_code == 200
        assert response.data["status"] == "in-progress"
        
    def test_update_wrong_status(self, admin_user: User, test_contact_form: ContactForm) -> None:
        url = f"{self.endpoint}{str(test_contact_form.id)}/status-change/"
        data = {"status": "dummy-status"}

        self.client.force_authenticate(
            user=admin_user
        )
        response = self.client.patch(url, data=data)
        assert response.status_code == 400
