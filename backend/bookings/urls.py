from django.urls import path
from .views import (
    MyTimeSlotListCreateView,
    AvailableTimeSlotsListView,
    BookingListCreateView,
    BookingDetailView,
)

app_name = "bookings"

urlpatterns = [
    # TimeSlots
    path("my-slots/", MyTimeSlotListCreateView.as_view(), name="my-slots"),
    path("slots/", AvailableTimeSlotsListView.as_view(), name="available-slots"),

    #Booking
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
]
