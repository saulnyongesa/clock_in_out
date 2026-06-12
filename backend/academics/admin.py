from django.contrib import admin

from academics.models import Term, Unit


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("name", "institution", "starts_on", "ends_on", "is_active")
    list_filter = ("institution", "is_active")
    search_fields = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "institution", "weekly_hours_target", "term_hours_target")
    list_filter = ("institution", "is_active")
    search_fields = ("code", "name")
