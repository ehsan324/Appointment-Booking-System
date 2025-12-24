from rest_framework import generics, status
from rest_framework.response import Response
from core.permissions import IsClient, IsProvider
from bookings.models import Booking
from bookings.services.booking_service import BookingService


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
