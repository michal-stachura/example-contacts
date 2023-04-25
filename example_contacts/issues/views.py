from django.shortcuts import render
from example_contacts.issues.forms import ContactForm

def contact_form(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to thank you page

    else:
        form = ContactForm()

    return render(request, 'contact_form.html', {'form': form})
