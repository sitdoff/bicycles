from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rent.models import BicycleModel, RentBicycleModel
from rent.serializers import RentBicycleSerializer
from rest_framework.test import APIRequestFactory

User = get_user_model()


@pytest.mark.django_db
def test_rent_bicycle_serializer_create():
    user = User.objects.create_user(username="testuser", password="testpass")

    bicycle = BicycleModel.objects.create(brand="Cannondale", cost_per_hour=Decimal("10.00"), is_rented=False)

    factory = APIRequestFactory()
    request = factory.post("/rent/", {}, format="json")
    request.user = user

    rent_data = {
        "bicycle": bicycle.id,
    }

    serializer = RentBicycleSerializer(data=rent_data, context={"request": request})
    assert serializer.is_valid()
    rent = serializer.save()

    assert rent.renter == user
    assert rent.bicycle == bicycle


@pytest.mark.django_db
def test_rent_bicycle_serializer_fields():
    user = User.objects.create_user(username="testuser", password="testpass")

    bicycle = BicycleModel.objects.create(brand="Cannondale", cost_per_hour=Decimal("10.00"), is_rented=False)

    start_time = timezone.now() - timedelta(hours=2)
    end_time = timezone.now()
    rent = RentBicycleModel.objects.create(bicycle=bicycle, renter=user, end_time=end_time)

    rent.start_time = start_time
    rent.save()

    serializer = RentBicycleSerializer(rent)
    data = serializer.data

    assert data["bicycle"] == bicycle.id
    assert data["renter"] == user.id
    assert data["cost"] == str(bicycle.cost_per_hour * Decimal(2))
    assert data["paid"] == rent.paid
    assert data["end_time"] == end_time.isoformat().replace("+00:00", "Z")


@pytest.mark.django_db
def test_rent_bicycle_serializer_invalid_data():
    user = User.objects.create_user(username="testuser", password="testpass")

    factory = APIRequestFactory()
    request = factory.post("/rent/", {}, format="json")
    request.user = user

    rent_data = {}

    serializer = RentBicycleSerializer(data=rent_data, context={"request": request})
    assert not serializer.is_valid()
    assert "bicycle" in serializer.errors
