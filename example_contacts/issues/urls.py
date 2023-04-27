from django.conf import settings
from django.urls import path
from example_contacts.issues.views import (
    contact_form,
    thankyou_page,
    contact_form_list,
    contact_form_detail,
    update_contact_form_status
)

app_name = "issues"

urlpatterns = [
    path("", contact_form, name="contact_form"),
    path("confirm/", thankyou_page, name="thank_you"),
    path("issues/", contact_form_list, name="contact_form_list"),
    path("issues/<uuid:uuid>/", contact_form_detail, name="contact_form_detail"),
    path("issues/<uuid:uuid>/status-change/", update_contact_form_status, name="update_contact_form_status"),
]
