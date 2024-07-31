from rest_framework import serializers

from .models import BicycleModel, RentBicycleModel


class BicycleSerializer(serializers.ModelSerializer):
    """
    Bicycle model serializer.
    """

    class Meta:
        model = BicycleModel
        fields = "__all__"


class RentBicycleSerializer(serializers.ModelSerializer):
    """
    Rent bicycle model serializer.
    """

    cost = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    paid = serializers.ReadOnlyField()
    renter = serializers.PrimaryKeyRelatedField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RentBicycleModel
        fields = "__all__"

    def create(self, validated_data):
        """
        Set renter field to current user.
        """
        request = self.context.get("request")
        user = request.user
        validated_data["renter"] = user
        return super().create(validated_data)


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for swagger.
    """

    error = serializers.CharField()
