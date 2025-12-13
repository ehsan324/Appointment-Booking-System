from django.db import models
from core.models import TimeStampedModel
from providers.models import ProviderProfile, Service
from django.conf import settings

class TimeSlot(TimeStampedModel):
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name="time_slots",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="time_slots",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.provider.display_name} - {self.start_datetime} → {self.end_datetime}"

    class Meta:
        ordering = ["start_datetime"]

class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELED = "CANCELED", "Canceled"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Booking by {self.client} for {self.slot}"

    class Meta:
        ordering = ["-created_at"]
