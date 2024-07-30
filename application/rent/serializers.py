from rest_framework import serializers

from .models import BicycleModel, RentBicycleModel


class BicycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BicycleModel
        fields = "__all__"


class RentBicycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = RentBicycleModel
        fields = "__all__"
