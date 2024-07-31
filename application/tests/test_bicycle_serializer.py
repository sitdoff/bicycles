from decimal import Decimal

import pytest
from rent.serializers import BicycleSerializer
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_bicycle_serializer_create(bicycle_data):
    serializer = BicycleSerializer(data=bicycle_data)
    assert serializer.is_valid()
    bicycle = serializer.save()

    assert bicycle.brand == bicycle_data["brand"]
    assert bicycle.cost_per_hour == Decimal(bicycle_data["cost_per_hour"])
    assert bicycle.is_rented == bicycle_data["is_rented"]


@pytest.mark.django_db
def test_bicycle_serializer_update(bicycle):
    updated_data = {"brand": "Trek", "cost_per_hour": "20.00", "is_rented": False}
    serializer = BicycleSerializer(bicycle, data=updated_data)
    assert serializer.is_valid()
    updated_bicycle = serializer.save()

    assert updated_bicycle.brand == updated_data["brand"]
    assert updated_bicycle.cost_per_hour == Decimal(updated_data["cost_per_hour"])
    assert updated_bicycle.is_rented == updated_data["is_rented"]


def test_bicycle_serializer_validation_error(bicycle_data):
    invalid_data = bicycle_data.copy()
    invalid_data["cost_per_hour"] = "invalid_decimal"

    serializer = BicycleSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_bicycle_serializer_data(bicycle):
    serializer = BicycleSerializer(bicycle)
    expected_data = {
        "id": bicycle.id,
        "brand": bicycle.brand,
        "cost_per_hour": str(bicycle.cost_per_hour),
        "is_rented": bicycle.is_rented,
    }
    assert serializer.data == expected_data
