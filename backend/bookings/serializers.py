from rest_framework import serializers
from .models import TimeSlot, Booking
from providers.models import ProviderProfile
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError
from bookings.services.booking_service import BookingService




class TimeSLotSerializer(serializers.ModelSerializer):
    provider_id = serializers.ReadOnlyField(source='provider.id')

    class Meta:
        model = TimeSlot
        fields = [
            "id",
            "provider_id",
            "service",
            "start_datetime",
            "end_datetime",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "provider_id", "created_at", "updated_at"]

    def validate(self, attrs):
        start = attrs.get("start_datetime")
        end = attrs.get("end_datetime")

        if start >= end:
            raise serializers.ValidationError("start_datetime must be before end_datetime.")

        if start < timezone.now():
            raise serializers.ValidationError("Cannot create a time slot in the past.")

        return attrs


class BookingSerializer(serializers.ModelSerializer):
    client_id = serializers.ReadOnlyField(source='client.id')
    slot_id = serializers.PrimaryKeyRelatedField(source='slot', queryset=TimeSlot.objects.all() , write_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "client_id",
            "slot_id",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "client_id", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        slot = validated_data["slot"]
        notes = validated_data.get("notes", "")

        return BookingService.create_booking(
            client=user,
            slot=slot,
            notes=notes,
        )