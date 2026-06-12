from django.contrib import admin

from attendance.models import AttendanceSession


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = (
        "trainer",
        "unit",
        "clock_in_at",
        "clock_out_at",
        "actual_minutes",
        "credited_minutes",
        "is_active",
    )
    list_filter = ("institution", "is_active", "unit")
    search_fields = ("trainer__name", "trainer__id_number", "unit__code", "unit__name")
