from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from rent.models import BicycleModel, RentBicycleModel
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_bicycles():
    BicycleModel.objects.create(brand="Cannondale", cost_per_hour=Decimal("10.00"), is_rented=False)
    BicycleModel.objects.create(brand="Trek", cost_per_hour=Decimal("12.00"), is_rented=True)
    BicycleModel.objects.create(brand="Specialized", cost_per_hour=Decimal("8.00"), is_rented=False)


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def bicycle():
    return BicycleModel.objects.create(brand="Cannondale", cost_per_hour=Decimal("10.00"), is_rented=False)


@pytest.fixture
def bicycle_data():
    return {"brand": "Cannondale", "cost_per_hour": "10.00", "is_rented": False}


@pytest.fixture
def create_rented_bicycle(user, bicycle):
    return RentBicycleModel.objects.create(bicycle=bicycle, renter=user, end_time=timezone.now() + timedelta(hours=1))


@pytest.fixture
def create_rent(user, create_bicycle):
    return RentBicycleModel.objects.create(bicycle=create_bicycle, renter=user, start_time=timezone.now())


@pytest.fixture
def mock_start_process_rent():
    with patch("rent.views.start_process_rent.delay") as mock:
        yield mock
