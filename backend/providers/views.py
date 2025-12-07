from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveUpdateAPIView
from .models import ProviderProfile, Service
from .serializers import ProviderProfileSerializer, ServiceSerializer
from .permissions import IsProviderOrReadOnly, IsServiceOwnerOrReadOnly, IsProvider
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class ProviderProfileListView(ListAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer
    permission_classes = [AllowAny]


class ProviderProfileDetailView(RetrieveAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer
    permission_classes = [AllowAny]


class MyProviderProfileView(RetrieveUpdateAPIView):

    serializer_class = ProviderProfileSerializer
    permission_classes = [IsProvider, IsAuthenticated]

    def get_object(self):
        user = self.request.user
        profile, created = ProviderProfile.objects.get_or_create(
            user=user,
            defaults={
                "display_name": user.username,
            },
        )
        return profile


class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsProviderOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'provider_profile'):
            raise ValidationError('No provider profile associated with this user.')

        serializer.save(provider=user.provider_profile)


class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsServiceOwnerOrReadOnly]
