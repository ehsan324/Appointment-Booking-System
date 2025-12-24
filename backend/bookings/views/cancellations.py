from rest_framework import generics, status
from rest_framework.response import Response
from core.permissions import IsClient, IsProvider
from bookings.models import Booking
from bookings.services.booking_service import BookingService
from drf_spectacular.utils import extend_schema, OpenApiResponse



@extend_schema(
    tags=["Bookings"],
    summary="Cancell of booking",
    description=(
            "Cancell an object "
            "This endpoint enforces business rules: \n"
            "- time slot must not already be booked\n"
            "- user must be owner"
    ),
    responses={
        201: OpenApiResponse(description="Cancelled Successfully"),
        400: OpenApiResponse(description="Validation error"),
        401: OpenApiResponse(description="Authentication required"),
        403: OpenApiResponse(description="Forbidden: only clients can cancell bookings"),
        429: OpenApiResponse(description="Too many requests (rate limit exceeded)"),
    })

class BookingCancelView(generics.GenericAPIView):
    queryset = Booking.objects.all()
    permission_classes = (IsClient | IsProvider)

    def post(self, request, pk):
        booking = self.get_object()
        BookingService.cancel_booking(
            booking=booking,
            by_user=request.user,
        )
        return Response({"detail": "Booking canceled."}, status=status.HTTP_200_OK)
