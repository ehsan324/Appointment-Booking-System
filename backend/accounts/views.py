from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .throttles import LoginAnonRateThrottle
from rest_framework.throttling import AnonRateThrottle
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginView(TokenObtainPairView):
    throttle_classes = (LoginAnonRateThrottle, AnonRateThrottle)

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)

