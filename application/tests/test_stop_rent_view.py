from decimal import Decimal

import pytest
from django.urls import reverse
from django.utils import timezone
from rent.models import BicycleModel, RentBicycleModel
from rest_framework import status


@pytest.fixture
def create_bicycle():
    return BicycleModel.objects.create(brand="Cannondale", cost_per_hour=Decimal("10.00"), is_rented=True)


@pytest.mark.django_db
def test_stop_rent_view_authenticated(api_client, user, create_rent):
    api_client.login(username="testuser", password="password")

    response = api_client.post(reverse("return"))

    assert response.status_code == status.HTTP_200_OK
    rent = RentBicycleModel.objects.get(pk=create_rent.pk)
    assert response.json() == {"success": "Bicycle returned", "rent": rent.pk}
    assert not rent.bicycle.is_rented


@pytest.mark.django_db
def test_stop_rent_view_unauthenticated(api_client):
    response = api_client.post(reverse("return"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_stop_rent_view_no_active_rent(api_client, user):
    api_client.login(username="testuser", password="password")

    response = api_client.post(reverse("return"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "No active rent"}
