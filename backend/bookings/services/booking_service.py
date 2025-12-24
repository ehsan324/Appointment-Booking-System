from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError

from bookings.models import Booking, TimeSlot


class BookingService:

    @staticmethod
    def create_booking(*, client, slot: TimeSlot, notes=""):

        if slot.start_datetime < timezone.now():
            raise DjangoValidationError("cannot book a past time slot.")

        if hasattr(slot, "booking"):
            raise DjangoValidationError("time slot is already booking.")

        if not client.is_client:
            raise DjangoValidationError("only client can book booking.")

        booking = Booking(
            client=client,
            slot=slot,
            notes=notes,
        )

        booking.full_clean()

        booking.save()

        return booking

    @staticmethod
    def cancel_booking(*, booking, by_user):

        if by_user != booking.client and by_user != booking.slot.provider.user:
            raise DjangoValidationError("cannot cancel booking by user")

        if booking.status == Booking.Status.CANCELED:
            raise DjangoValidationError("already canceled")

        booking.status = Booking.Status.CANCELED
        booking.save()

        return booking


