from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from bookings.models import TimeSlot, Booking
from bookings.serializers import TimeSLotSerializer, BookingSerializer
from core.permissions import IsProvider, IsClient
from datetime import datetime
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    tags=["Slots"],
    summary="Create Your SLots",
    description="Create & Add your Slot for seeing Client",
    responses={
        201: TimeSLotSerializer,
        400: OpenApiResponse(description="Invalid Inputs"),
        429: OpenApiResponse(description="Too many attempts (rate limit)"),
    }
)

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

@extend_schema(
    tags=["Slots"],
    summary="List of Available Slots",
    description="Return And Show List of Available Slots for Client",
    responses={
        200: OpenApiResponse(description="Returned Successfully"),
        401: OpenApiResponse(description="Authentication required"),
        404: OpenApiResponse(description="No TimeSLot found"),
        429: OpenApiResponse(description="Too many attempts (rate limit)"),
    }
)
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
