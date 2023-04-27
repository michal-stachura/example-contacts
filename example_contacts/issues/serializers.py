from rest_framework import serializers
from example_contacts.issues.models import ContactForm

class ContactFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactForm
        fields = [
            "id",
            "name",
            "subject",
            "status",
            "email"
        ]

class ContactFormDetailSerializer(ContactFormSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_fields = ContactFormSerializer.Meta.fields + [
            "message"
        ]
        excluded_fields = self.context.get("excluded_fields", [])
        self.Meta.fields = list(set(base_fields) - set(excluded_fields))
