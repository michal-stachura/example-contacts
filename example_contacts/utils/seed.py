import random
from faker import Faker
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from example_contacts.issues.models import ContactForm
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()
env_name = settings.ENV_NAME or None


if env_name == "local" and not User.objects.filter(username="admin").exists():
    print("-" * 8)
    print ("Create local superuser")
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin"
    )
    print ("Local super user created: login: admin, password: admin")
    print("-" * 8)

print ("Create 50000 Random Issues. Please wait...")
subject_choices = [choice[0] for choice in ContactForm.SUBJECT_CHOICES]
status_choices = [choice[0] for choice in ContactForm.STATUS_CHOICES]

bulk_list = [
    ContactForm(
        name = fake.name(),
        email = fake.email(),
        subject = random.choice(subject_choices),
        message = fake.text(max_nb_chars = 500),
        status = random.choice(status_choices),
    )
    for x in range(50000)
]
ContactForm.objects.bulk_create(bulk_list, batch_size=10000)

contact_forms = ContactForm.objects.all()
contact_forms_to_update = []
for cf in contact_forms:
    cf.created_at = fake.date_time_this_century(before_now=True, after_now=False, tzinfo=timezone.get_current_timezone())
    contact_forms_to_update.append(cf)
    if cf.status != "new":
        cf.updated_at = cf.updated_at + timedelta(hours=1)

ContactForm.objects.bulk_update(contact_forms_to_update, ["created_at"], batch_size=10000)
print ("Done. Please run 'sudo make run' and open http://127.0.0.1:8080/")
print("-" * 8)