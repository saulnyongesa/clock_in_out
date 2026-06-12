from django.contrib import admin

from institutions.models import Institution


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "clock_out_allowance_minutes")
    search_fields = ("name", "email", "phone")
