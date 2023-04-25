from django.conf import settings
from django.urls import path
from example_contacts.issues.views import contact_form, thankyou_page

app_name = "issues"

urlpatterns = [
    path("", contact_form, name="contact_form"),
    path("/confirm", thankyou_page, name="thank_you")
]
