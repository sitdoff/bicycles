from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rent.tasks import start_process_rent
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BicycleModel, RentBicycleModel
from .serializers import (
    BicycleSerializer,
    ErrorResponseSerializer,
    RentBicycleSerializer,
)

# Create your views here.
User = get_user_model()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="List of available bicycles",
                schema=BicycleSerializer(many=True),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                    example={"detail": "Authentication credentials were not provided."},
                ),
            ),
        },
    ),
)
class AllBicycleView(ListAPIView):
    """
    Displays all available bikes
    """

    queryset = BicycleModel.objects.filter(is_rented=False)
    serializer_class = BicycleSerializer
    permission_classes = (IsAuthenticated,)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="List of available bicycles",
                schema=BicycleSerializer(many=True),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                    example={"detail": "Authentication credentials were not provided."},
                ),
            ),
        },
    ),
)
class RentBicycleView(ListCreateAPIView):
    """
    Displays all bikes that were rented
    """

    serializer_class = RentBicycleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[BicycleModel]:
        return self.request.user.rented_bicycles.select_related("bicycle").order_by("-end_time")

    @swagger_auto_schema(
        responses={
            201: openapi.Response(
                description="Rent created successfully",
                schema=RentBicycleSerializer,
            ),
            400: openapi.Response(
                description="Error during rent creation",
                schema=ErrorResponseSerializer,
                examples={
                    "application/json": [
                        {"error": "Bicycle is not available"},
                        {"error": "You have already rented a bike"},
                    ]
                },
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                    example={"detail": "Authentication credentials were not provided."},
                ),
            ),
        },
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Creates a new rent.
        """
        if BicycleModel.objects.get(pk=request.data["bicycle"]).is_rented:
            return Response({"error": "Bicycle is not available"}, status=400)

        if request.user.rented_bicycles.filter(end_time=None).exists():
            return Response({"error": "You have already rented a bike"}, status=400)

        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            instanse: RentBicycleModel = serializer.save()
            start_process_rent.delay(instanse.pk, instanse.bicycle.pk)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class StopRentView(APIView):
    """
    Stop rent time.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: '{"success": "Bicycle returned", "rent": {rent.pk}}',
            401: openapi.Response(
                description="Authentication credentials were not provided.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"detail": openapi.Schema(type=openapi.TYPE_STRING)},
                    example={"detail": "Authentication credentials were not provided."},
                ),
            ),
            404: "No active rent",
        }
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        rent: RentBicycleModel = request.user.rented_bicycles.filter(end_time=None).first()
        if not rent:
            return Response({"error": "No active rent"}, status=404)
        bicycle = rent.bicycle
        bicycle.is_rented = False
        bicycle.save()
        return Response({"success": "Bicycle returned", "rent": rent.pk}, status=200)
