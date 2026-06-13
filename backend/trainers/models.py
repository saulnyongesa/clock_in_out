from django.db import models

from academics.models import Unit
from institutions.models import Institution


class Trainer(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=160)
    id_number = models.CharField(max_length=60, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to="trainer_photos/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    units = models.ManyToManyField(Unit, through="TrainerUnit", related_name="trainers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = self.name.upper().strip()
        self.id_number = self.id_number.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.id_number})"


class TrainerUnit(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trainer", "unit")

    def __str__(self):
        return f"{self.trainer} -> {self.unit}"
