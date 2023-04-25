from django import forms
from example_contacts.issues.models import ContactForm

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
