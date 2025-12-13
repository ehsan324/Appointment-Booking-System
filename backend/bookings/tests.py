from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model
from providers.models import ProviderProfile, Service
from .models import TimeSlot, Booking

User = get_user_model()


class BookingTestBase(TestCase):
    def setUp(self):
        self.provider_user = User.objects.create_user(
            username="provider1",
            password="test1234",
            role=User.Roles.PROVIDER,
        )
        self.provider_profile = ProviderProfile.objects.create(
            user=self.provider_user,
            display_name="Dr. Test",
        )
        self.service = Service.objects.create(
            provider=self.provider_profile,
            name="Consultation",
            duration_minutes=30,
        )

        self.client_user = User.objects.create_user(
            username="client1",
            password="test1234",
            role=User.Roles.CLIENT,
        )

        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(minutes=30)
        self.slot = TimeSlot.objects.create(
            provider=self.provider_profile,
            service=self.service,
            start_datetime=start,
            end_datetime=end,
        )


class BookingModelTests(BookingTestBase):
    def test_cannot_double_book_same_slot(self):
        Booking.objects.create(client=self.client_user, slot=self.slot)

        with self.assertRaises(Exception):
            Booking.objects.create(client=self.client_user, slot=self.slot)


class BookingApiTests(BookingTestBase):
    def setUp(self):
        super().setUp()
        self.api_client = APIClient()
        self.api_client.raise_request_exception = True

    def authenticate_as_client(self):
        response = self.api_client.post(
            "/auth/login/",
            {
                "username": "client1", "password": "test1234"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_client_can_create_booking_for_free_slot(self):
        self.authenticate_as_client()

        response = self.api_client.post(
            "/bookings/bookings/",
            {
                "slot_id": self.slot.id, "notes": "first session"
            }, format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.slot, self.slot)
        self.assertEqual(booking.client, self.client_user)

    def test_cannot_book_already_booked_slot(self):
        Booking.objects.create(client=self.client_user, slot=self.slot)

        self.authenticate_as_client()
        response = self.api_client.post(
            "/bookings/bookings/",
            {"slot_id": self.slot.id, "notes": "Second try"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", response.data)


class AvailableSlotApiTests(BookingTestBase):
    def setUp(self):
        super().setUp()
        self.api_client = APIClient()
        self.api_client.raise_request_exception = True

    def test_available_slots_excludes_booked_slots(self):

        response_1 = self.api_client.get("/bookings/slots/")
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_1.data), 1)

        Booking.objects.create(client=self.client_user, slot=self.slot)

        response_2 = self.api_client.get("/bookings/slots/")
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(len(response_2.data), 0)
