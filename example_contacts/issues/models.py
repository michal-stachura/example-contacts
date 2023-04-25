from django.db import models
from django.utils.translation import gettext_lazy as _
from example_contacts.utils.common_model import CommonModel

class ContactForm(CommonModel):
    SUBJECT_CHOICES = (
        ("app-support", _("App Support")),
        ("payment-support", _("Payment Support")),
        ("hr-jobs", _("HR/Jobs")),
        ("other", _("Other")),
    )
    STATUS_CHOICES = (
        ("new", _("New")),
        ("in-progress", _("In-Progress")),
        ("resolved", _("Resolved")),
    )
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    subject = models.CharField(
        choices=SUBJECT_CHOICES,
        max_length=50,
        default="app_support"
    )
    message = models.TextField(max_length=500)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="new"
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__regex=r"^.{5,}$"),
                name="%(app_label)s_%(class)s_min_name_length",
                violation_error_message=_("Name must be minimum 5 letters long."),
            )
        ]
    
    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"
