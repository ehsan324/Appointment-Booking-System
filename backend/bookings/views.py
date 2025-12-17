# bookings/views.py
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import TimeSlot, Booking
from .serializers import TimeSLotSerializer, BookingSerializer
from .permissions import IsBookingOwner
from core.permissions import IsProvider, IsClient
from django.db.models import Exists, OuterRef
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .throttles import BookingCreateRateThrottle

import logging

logger = logging.getLogger("booking_app")


class MyTimeSlotListCreateView(generics.ListCreateAPIView):
    serializer_class = TimeSLotSerializer

    permission_classes = (permissions.IsAuthenticated, IsProvider)

    def get_queryset(self):
        user = self.request.user
        return TimeSlot.objects.filter(provider__user=user).order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, "provider_profile"):
            raise ValidationError("NO PROVIDER PROFILE")

        serializer.save(provider=user.provider_profile)


class AvailableTimeSlotsListView(generics.ListAPIView):
    serializer_class = TimeSLotSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        qs = TimeSlot.objects.future().available()

        provider_id = self.request.query_params.get("provider_id")
        if provider_id:
            qs = qs.filter(provider_id=provider_id)

        date_str = self.request.query_params.get("date")
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str).date()
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

            qs = qs.filter(start_datetime__date=date_obj)

        return qs.order_by("start_datetime")


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
