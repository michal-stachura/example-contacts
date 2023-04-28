import pytest

from example_contacts.issues.models import ContactForm
from example_contacts.issues.tests.factories import ContactFormFactory

@pytest.fixture
def contact_form_fixture(db) -> ContactForm:
    return ContactFormFactory()
