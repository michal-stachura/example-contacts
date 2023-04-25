# Generated by Django 4.1.8 on 2023-04-25 06:16

import dirtyfields.dirtyfields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactForm",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=150)),
                (
                    "subject",
                    models.CharField(
                        choices=[
                            ("app-support", "App Support"),
                            ("payment-support", "Payment Support"),
                            ("hr-jobs", "HR/Jobs"),
                            ("other", "Other"),
                        ],
                        default="app_support",
                        max_length=50,
                    ),
                ),
                ("message", models.TextField(max_length=500)),
                (
                    "status",
                    models.CharField(
                        choices=[("new", "New"), ("in-progress", "In-Progress"), ("resolved", "Resolved")],
                        default="new",
                        max_length=50,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name="contactform",
            constraint=models.CheckConstraint(
                check=models.Q(("name__regex", "^.{5,}$")),
                name="issues_contactform_min_name_length",
                violation_error_message="Name must be minimum 5 letters long.",
            ),
        ),
    ]
