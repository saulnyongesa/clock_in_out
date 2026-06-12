from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from academics.api import UnitViewSet
from attendance.api import AttendanceSessionViewSet
from config.views import health_check
from institutions.api import InstitutionViewSet
from trainers.api import TrainerViewSet


router = DefaultRouter()
router.register("institutions", InstitutionViewSet)
router.register("units", UnitViewSet)
router.register("trainers", TrainerViewSet)
router.register("attendance-sessions", AttendanceSessionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health_check, name="health-check"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
