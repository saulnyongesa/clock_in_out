from django.db import models
from django.core.validators import MinValueValidator


class Institution(models.Model):
    name = models.CharField(max_length=160, unique=True)
    logo = models.ImageField(upload_to="institution_logos/", blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    clock_out_allowance_minutes = models.PositiveSmallIntegerField(default=10)
    default_class_minutes = models.PositiveSmallIntegerField(
        default=60,
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
