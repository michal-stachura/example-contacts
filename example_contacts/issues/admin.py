from django.contrib import admin
from example_contacts.issues.models import ContactForm

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "status",)
    list_filter = ("status",)
    search_fields = ("email", "name")
