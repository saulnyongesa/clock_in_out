from django.contrib import admin

from trainers.models import Trainer, TrainerUnit


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("name", "id_number", "institution", "phone", "is_active")
    list_filter = ("institution", "is_active")
    search_fields = ("name", "id_number", "phone", "email")
    readonly_fields = ("pin_hash",)


@admin.register(TrainerUnit)
class TrainerUnitAdmin(admin.ModelAdmin):
    list_display = ("trainer", "unit", "created_at")
    search_fields = ("trainer__name", "trainer__id_number", "unit__code", "unit__name")
