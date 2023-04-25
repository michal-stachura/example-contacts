from django.shortcuts import render, redirect
from example_contacts.issues.forms import ContactForm

def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("issues:thank_you")
            
    else:
        form = ContactForm()

    return render(request, "contact_form.html", {"form": form})


def thankyou_page(request):
    return render(request, "thank_you_page.html")
