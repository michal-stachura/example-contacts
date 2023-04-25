from django.conf import settings
from django.urls import path
from example_contacts.issues.views import contact_form

app_name = "issues"

urlpatterns = [
    path("", contact_form, name="contact_form")
]
