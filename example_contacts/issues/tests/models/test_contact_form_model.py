import pytest
import uuid
from django.db.utils import IntegrityError
from django.db.transaction import TransactionManagementError

from example_contacts.issues.models import ContactForm
from example_contacts.issues.tests.factories import ContactFormFactory
from example_contacts.issues.tests.fixtures import contact_form_fixture

pytestmark = pytest.mark.django_db
test_contact_form = contact_form_fixture

class TestContactFormModel:
    def test_contact_form_add(self) -> None:
        contact_form = ContactFormFactory()
        assert contact_form.id != ""
        assert type(contact_form.id) == uuid.UUID
        assert ContactForm.objects.all().count() == 1

    def test_read_db(self, test_contact_form: ContactForm) -> None:
        obj = ContactForm.objects.get(id=test_contact_form.id)
        assert test_contact_form == obj
    
    def test_soft_delete(self) -> None:
        ContactFormFactory.create_batch(10)
        cf_to_delete = ContactFormFactory()

        assert ContactForm.objects.all().count() == 11
        cf_to_delete.delete()

        assert ContactForm.objects.all().count() == 10
        assert ContactForm.objects.with_deleted().count() == 11
        assert not ContactForm.objects.filter(id=str(cf_to_delete.id)).exists()
        assert ContactForm.objects.with_deleted().filter(id=str(cf_to_delete.id)).count() == 1

    def test_hard_delete(self) -> None:
        ContactFormFactory.create_batch(10)
        cf_to_delete = ContactFormFactory()

        assert ContactForm.objects.all().count() == 11
        cf_to_delete.delete_forever()

        assert ContactForm.objects.all().count() == 10
        assert ContactForm.objects.with_deleted().count() == 10

    def test_status_newly_created_objects(self) -> None:
        contact_form = ContactFormFactory(
            status = "in-progress"
        )

        assert contact_form.status == "new"

    def test_update_status(self) -> None:
        contact_form = ContactFormFactory()
        assert contact_form.status == "new"

        contact_form.status = "in-progress"
        contact_form.save()  # save method with "is_being_created" == False

        assert contact_form.status == "in-progress"

    def test_constraints_min_name_length(self) -> None:
        with pytest.raises((IntegrityError, TransactionManagementError,)):
            ContactFormFactory(
                name = "Mic"
            )
            assert ContactForm.objects.all().count() == 0
