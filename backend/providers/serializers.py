from rest_framework import serializers
from .models import ProviderProfile, Service


class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = [
            "id",
            "display_name",
            "bio",
            "location",
        ]

class ServiceSerializer(serializers.ModelSerializer):
    provider_id = serializers.ReadOnlyField(source="provider.id")

    class Meta:
        model = Service
        fields = [
            "id",
            "provider_id",
            "name",
            "description",
            "duration_minutes",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "provider_id", "created_at", "updated_at"]
        