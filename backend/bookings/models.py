from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError

from core.models import TimeStampedModel
from providers.models import ProviderProfile, Service
from django.conf import settings


class BookingManager(models.Manager):
    def create_booking(self, *, client, slot, notes=""):
        if slot.start_datetime < timezone.now():
            raise ValidationError("Cant book a past time slot.")

        if Booking.objects.filter(slot=slot).exists():
            raise ValidationError("Slot already booking.")

        booking = self.model(
            client=client,
            slot=slot,
            notes=notes,
        )
        booking.full_clean()
        booking.save()
        return booking


class TimeSlotQuerySet(models.QuerySet):
    def future(self):
        return self.filter(start_datetime__gte=timezone.now())

    def available(self):
        from .models import Booking

        return self.annotate(
            has_booking=Exists(
                Booking.objects.filter(slot=OuterRef('pk'))
            )
        ).filter(has_booking=False)


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

    objects = TimeSlotQuerySet.as_manager()

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

    objects = BookingManager()

    def __str__(self):
        return f"Booking by {self.client} for {self.slot}"

    class Meta:
        ordering = ["-created_at"]
