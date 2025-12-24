from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    tags=["Health"],
    summary="Health check endpoint",
    description="Useful for readiness/liveness probes in Docker/K8s.",
    responses={200: OpenApiResponse(description="Service operational")},
)
class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "status": "OK",
        })
