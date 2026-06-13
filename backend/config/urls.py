from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from academics.api import UnitViewSet
from attendance.api import AttendanceSessionViewSet
from config.views import (
    active_classes_page,
    assignments_page,
    attendance_history_page,
    clock_page,
    export_attendance_report,
    export_trainer_summary,
    export_unit_summary,
    health_check,
    landing_page,
    monitor_dashboard,
    network_info,
    reports_page,
    setup_page,
    trainers_page,
    units_page,
    web_dashboard,
)
from institutions.api import InstitutionViewSet, current_institution
from trainers.api import TrainerViewSet


router = DefaultRouter()
router.register("institutions", InstitutionViewSet)
router.register("units", UnitViewSet)
router.register("trainers", TrainerViewSet)
router.register("attendance-sessions", AttendanceSessionViewSet)

urlpatterns = [
    path("", landing_page, name="landing-page"),
    path("app/", web_dashboard, name="web-dashboard"),
    path("app/setup/", setup_page, name="setup-page"),
    path("app/system/monitor/", monitor_dashboard, name="monitor-dashboard"),
    path("app/trainers/", trainers_page, name="trainers-page"),
    path("app/units/", units_page, name="units-page"),
    path("app/assignments/", assignments_page, name="assignments-page"),
    path("app/active-classes/", active_classes_page, name="active-classes-page"),
    path("app/attendance/", attendance_history_page, name="attendance-history-page"),
    path("app/reports/", reports_page, name="reports-page"),
    path("app/reports/export/attendance/", export_attendance_report, name="export-attendance-report"),
    path("app/reports/export/trainers/", export_trainer_summary, name="export-trainer-summary"),
    path("app/reports/export/units/", export_unit_summary, name="export-unit-summary"),
    path("trainer/clock/", clock_page, name="clock-page"),
    path("admin/", admin.site.urls),
    path("api/health/", health_check, name="health-check"),
    path("api/network/", network_info, name="network-info"),
    path("api/institution-setup/current/", current_institution, name="current-institution"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
