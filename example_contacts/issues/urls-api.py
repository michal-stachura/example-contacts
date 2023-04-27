from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from example_contacts.issues.views import ContactFormViewSet
app_name = "issues"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", ContactFormViewSet)

urlpatterns = router.urls
