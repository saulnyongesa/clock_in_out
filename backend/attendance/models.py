from decimal import Decimal

from django.db import models
from django.utils import timezone

from academics.models import Unit
from institutions.models import Institution
from trainers.models import Trainer


class AttendanceSession(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    clock_in_at = models.DateTimeField(default=timezone.now)
    clock_out_at = models.DateTimeField(blank=True, null=True)
    actual_minutes = models.PositiveIntegerField(blank=True, null=True)
    credited_minutes = models.PositiveIntegerField(blank=True, null=True)
    roll = models.CharField(max_length=50, blank=True)
    clock_in_photo = models.ImageField(upload_to="attendance_audit/")
    clock_out_photo = models.ImageField(upload_to="attendance_audit/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-clock_in_at"]
        indexes = [
            models.Index(fields=["trainer", "is_active"]),
            models.Index(fields=["unit", "clock_in_at"]),
        ]

    def clock_out(self, when=None):
        self.clock_out_at = when or timezone.now()
        seconds = max(0, int((self.clock_out_at - self.clock_in_at).total_seconds()))
        self.actual_minutes = seconds // 60
        self.credited_minutes = self.calculate_credited_minutes()
        self.is_active = False

    def calculate_credited_minutes(self):
        expected = int(self.unit.class_minutes or self.institution.default_class_minutes)
        allowance = int(self.institution.clock_out_allowance_minutes or 0)

        if self.actual_minutes is None:
            return None

        missing_minutes = expected - self.actual_minutes
        if 0 <= missing_minutes <= allowance:
            return expected
        return self.actual_minutes

    @property
    def credited_hours(self):
        if self.credited_minutes is None:
            return Decimal("0")
        return Decimal(self.credited_minutes) / Decimal("60")

    def __str__(self):
        return f"{self.trainer} - {self.unit} at {self.clock_in_at:%Y-%m-%d %H:%M}"
