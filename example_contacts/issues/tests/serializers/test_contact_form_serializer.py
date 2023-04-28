import pytest
from factory import build

from example_contacts.issues.serializers import (
    ContactFormSerializer,
    ContactFormDetailSerializer
)
from example_contacts.issues.tests.factories import ContactFormFactory
from example_contacts.issues.tests.fixtures import contact_form_fixture

pytestmark = pytest.mark.django_db
test_contact_form = contact_form_fixture

class TestContactFormSerializer:

    def test_seialize_model(self) -> None:
        contact_form = ContactFormFactory()
        serializer = ContactFormSerializer(contact_form)

        assert serializer.data
        assert set(serializer.data.keys()) == set([
            "id",
            "name",
            "subject",
            "status",
            "email"
            ]
        )

    def test_serialize_data(self) -> None:
        valid_serialized_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )

        serializer = ContactFormSerializer(
            data = valid_serialized_data
        )

        assert serializer.is_valid()
        assert serializer.errors == {}

        invalid_serialized_data = valid_serialized_data.pop("status")

        serializer = ContactFormSerializer(
            data = invalid_serialized_data
        )

        assert not serializer.is_valid()
        assert serializer.errors != {}

class TestContactFormDetailSerializer:

    def test_seialize_model(self) -> None:
        contact_form = ContactFormFactory()
        serializer = ContactFormDetailSerializer(contact_form)

        assert serializer.data
        assert set(serializer.data.keys()) == set([
            "id",
            "name",
            "subject",
            "status",
            "email",
            "message"
            ]
        )

    def test_serialize_data(self) -> None:
        valid_serialized_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )

        serializer = ContactFormDetailSerializer(
            data = valid_serialized_data
        )

        assert serializer.is_valid()
        assert serializer.errors == {}

        invalid_serialized_data = valid_serialized_data
        invalid_serialized_data.pop("message")
        serializer = ContactFormDetailSerializer(
            data = invalid_serialized_data
        )

        assert not serializer.is_valid()
        assert serializer.errors != {}

    
    def test_exclude_fields(self) -> None:
        invalid_serialized_data = build(
            dict,
            FACTORY_CLASS=ContactFormFactory
        )
        invalid_serialized_data.pop("message")
        
        serializer = ContactFormDetailSerializer(
            data = invalid_serialized_data
        )
        assert not serializer.is_valid()
        assert str(serializer.errors) == "{'message': [ErrorDetail(string='This field is required.', code='required')]}"

        serializer = ContactFormDetailSerializer(
            data = invalid_serialized_data,
            context={
                "excluded_fields": ["message"]
            }
        )
        
        assert serializer.is_valid()
        assert serializer.errors == {}

        