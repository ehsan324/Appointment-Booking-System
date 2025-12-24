from django.urls import path
from bookings.view.bookings import BookingListCreateView, BookingDetailView
from bookings.view.slots import AvailableTimeSlotsListView, MyTimeSlotListCreateView
from bookings.view.cancellations import BookingCancelView

app_name = "bookings"

urlpatterns = [
    # TimeSlots
    path("my-slots/", MyTimeSlotListCreateView.as_view(), name="my-slots"),
    path("slots/", AvailableTimeSlotsListView.as_view(), name="available-slots"),

    #Booking
    path("bookings/", BookingListCreateView.as_view(), name="booking-list-create"),
    path("bookings/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    path("bookings/<int:pk>/cancel/", BookingCancelView.as_view(), name="booking-cancel"),

]
