from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BicycleModel, RentBicycleModel
from .serializers import BicycleSerializer, RentBicycleSerializer
from .tasks import start_process_rent

# Create your views here.
User = get_user_model()


class AllBicycleView(ListAPIView):
    """
    Displays all available bikes
    """

    queryset = BicycleModel.objects.filter(is_rented=False)
    serializer_class = BicycleSerializer
    permission_classes = (IsAuthenticated,)


class RentBicycleView(ListCreateAPIView):
    """
    Displays all bikes that were rented
    """

    serializer_class = RentBicycleSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[BicycleModel]:
        return self.request.user.rented_bicycles.order_by("-end_time")

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

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        rent: RentBicycleModel = request.user.rented_bicycles.filter(end_time=None).first()
        bicycle = rent.bicycle
        bicycle.is_rented = False
        bicycle.save()
        return Response({"success": "Bike returned", "rent": rent.pk}, status=200)
