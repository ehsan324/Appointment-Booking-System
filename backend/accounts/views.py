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
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import UserSerializer

User = get_user_model()

@extend_schema(
    tags=["Auth"],
    summary="Authenticate user and return JWT tokens",
    description="Returns access + refresh tokens for a valid username/password.",
    responses={
        200: OpenApiResponse(description="JWT tokens successfully generated"),
        400: OpenApiResponse(description="Invalid credentials"),
        429: OpenApiResponse(description="Too many attempts (rate limit)"),
    }
)
class LoginView(TokenObtainPairView):
    throttle_classes = (LoginAnonRateThrottle, AnonRateThrottle)

@extend_schema(
    tags=["Auth"],
    summary="Register AND Get JWT tokens",
    description="Create User with Some Roll",
    responses={
        201: OpenApiResponse(description="User Created"),
        400: OpenApiResponse(description="Invalid Inputs"),
        429: OpenApiResponse(description="Too many attempts (rate limit)"),
    }
)
class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


@extend_schema(
    tags=["Auth"],
    summary="Get current authenticated user",
    responses={200: UserSerializer},
)
class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)

