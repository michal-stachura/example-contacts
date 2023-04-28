from factory import Faker, fuzzy
from factory.django import DjangoModelFactory

from example_contacts.issues.models import ContactForm

class ContactFormFactory(DjangoModelFactory):
    class Meta:
        model = ContactForm

    name = Faker("name")
    email = Faker("email")
    subject = fuzzy.FuzzyChoice(
        [choice[0] for choice in ContactForm.SUBJECT_CHOICES]
    )
    message = Faker("text", max_nb_chars=500)
    status = fuzzy.FuzzyChoice(
        [choice[0] for choice in ContactForm.STATUS_CHOICES]
    )
