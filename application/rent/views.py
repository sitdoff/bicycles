from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import BicycleModel, RentBicycleModel
from .serializers import BicycleSerializer, RentBicycleSerializer

# Create your views here.
User = get_user_model()


class AllBicycleView(ListAPIView):
    """
    Displays all available bikes
    """

    queryset = BicycleModel.objects.filter(is_rented=False)
    serializer_class = BicycleSerializer


class RentBicycleView(ListCreateAPIView):
    serializer_class = RentBicycleSerializer

    def get_queryset(self) -> QuerySet[BicycleModel]:
        return self.request.user.rented_bicycles

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if request.user.rented_bicycles.filter(end_time=None).exists():
            return Response({"error": "You have already rented a bike"}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
