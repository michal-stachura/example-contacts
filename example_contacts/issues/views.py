from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from example_contacts.issues.forms import ContactForm as CForm
from example_contacts.issues.models import ContactForm
from example_contacts.issues.serializers import (
    ContactFormSerializer,
    ContactFormDetailSerializer
)

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

# Api Views
class ContactFormViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
):
    queryset = ContactForm.objects.all()
    lookup_field = "id"
    
    def get_serializer_class(self):
        if self.action in ["retrieve", "create"]:
            return ContactFormDetailSerializer
        return ContactFormSerializer
    
    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(
        detail=True, methods=["patch"], url_path="status-change", url_name="status-change"
    )
    def update_status(self, request, *args, **kwargs):
        cf = self.get_object()
        cf_status = request.data.get("status", None)
        serializer = self.get_serializer(
            cf,
            data={"status": cf_status},
            partial=True,
            context={
                "excluded_fields": [
                    "id",
                    "name",
                    "subject",
                    "email",
                    "message",
                ]
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Common views
def contact_form(request):
    if request.method == "POST":
        form = CForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("issues:thank_you")
            
    else:
        form = CForm()

    return render(request, "contact_form.html", {"form": form})


def thankyou_page(request):
    return render(request, "thank_you_page.html")


@user_passes_test(lambda user: user.is_superuser)
def contact_form_list(request):
    contact_forms = ContactForm.objects.all()
    paginator = Paginator(contact_forms, settings.PAGE_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "contact_form_list.html",
        {
            "contact_forms": page_obj
        }
    )

@user_passes_test(lambda user: user.is_superuser)
def contact_form_detail(request, uuid):
    contact_form = get_object_or_404(ContactForm, id=uuid)
    return render(request, "contact_form_detail.html", {"contact_form": contact_form})


@user_passes_test(lambda user: user.is_superuser)
@require_POST
def update_contact_form_status(request, uuid):
    contact_form = get_object_or_404(ContactForm, id=uuid)
    new_status = request.POST.get('status')
    if new_status:
        contact_form.status = new_status
        contact_form.save()
    return redirect("issues:contact_form_list")