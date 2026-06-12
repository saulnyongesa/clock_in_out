from django.db import models
from django.core.validators import MinValueValidator

from institutions.models import Institution


class Term(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    starts_on = models.DateField()
    ends_on = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-starts_on"]
        unique_together = ("institution", "name")

    def __str__(self):
        return self.name


class Unit(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    code = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    class_minutes = models.PositiveSmallIntegerField(default=60)
    weekly_hours_target = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    term_hours_target = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("institution", "code")

    def save(self, *args, **kwargs):
        self.code = self.code.upper().strip()
        self.name = self.name.upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"
