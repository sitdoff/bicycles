from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone
from rent.models import RentBicycleModel


@pytest.mark.django_db
def test_create_rent_bicycle(user, bicycle):
    rent = RentBicycleModel.objects.create(bicycle=bicycle, renter=user)
    assert rent.bicycle == bicycle
    assert rent.renter == user
    assert rent.start_time is not None
    assert rent.end_time is None
    assert rent.paid is False


@pytest.mark.django_db
def test_rent_bicycle_cost(user, bicycle):
    end_time = timezone.now() + timedelta(hours=1)
    rent = RentBicycleModel.objects.create(bicycle=bicycle, renter=user, end_time=end_time)

    assert rent.start_time is not None
    assert rent.start_time < end_time

    expected_cost = bicycle.cost_per_hour
    assert rent.cost == expected_cost

    start_time = rent.start_time
    end_time = start_time + timedelta(hours=2)
    rent.end_time = end_time
    rent.save()

    expected_cost = bicycle.cost_per_hour * Decimal("2.00")
    assert rent.cost == expected_cost

    assert rent.start_time < rent.end_time


@pytest.mark.django_db
def test_rent_bicycle_cost_no_end_time(user, bicycle):
    rent = RentBicycleModel.objects.create(bicycle=bicycle, renter=user)
    assert rent.cost is None
