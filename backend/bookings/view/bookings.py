from rest_framework import generics, permissions
from bookings.models import TimeSlot, Booking
from bookings.serializers import TimeSLotSerializer, BookingSerializer
from bookings.permissions import IsBookingOwner
from core.permissions import IsProvider, IsClient
from drf_spectacular.utils import extend_schema, OpenApiResponse
from bookings.throttles import BookingCreateRateThrottle
import logging

logger = logging.getLogger("booking_app")


@extend_schema(
    tags=["bookings"],
    summary="List and create bookings for the current client",
    description=(
            "Returns the list of bookings for the authenticated client. "
            "Allows creating a new booking for a given time slot."
    ),
    responses={
        200: BookingSerializer,
        201: BookingSerializer,
        400: OpenApiResponse(
            description="Validation error (e.g. slot already booked or in the past)"
        ),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Only clients are allowed to create bookings"),
        429: OpenApiResponse(description="Too many requests (rate limit exceeded)"),

    },
)
class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]
    throttle_classes = [BookingCreateRateThrottle]

    def get_queryset(self):
        user = self.request.user
        result = Booking.objects.filter(client=user).order_by("-created_at")
        if result:
            logger.info(
                "New booking created",
                extra={
                    "client_id": self.request.user.id,
                },
            )

        return result


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient, IsBookingOwner]
