from unittest.mock import patch

import pytest
from django.urls import reverse
from rent.models import RentBicycleModel
from rent.serializers import RentBicycleSerializer
from rest_framework import status


@pytest.mark.django_db
def test_rent_bicycle_view_authenticated(api_client, user, create_rented_bicycle):
    api_client.login(username="testuser", password="password")

    response = api_client.get(reverse("rent"))

    assert response.status_code == status.HTTP_200_OK
    expected_data = RentBicycleSerializer(user.rented_bicycles.order_by("-end_time"), many=True).data
    assert response.json() == expected_data


@pytest.mark.django_db
def test_rent_bicycle_view_unauthenticated(api_client):
    response = api_client.get(reverse("rent"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_rent_bicycle_view_create_rent(api_client, user, bicycle, mock_start_process_rent):
    api_client.login(username="testuser", password="password")

    data = {"bicycle": bicycle.id}

    response = api_client.post(reverse("rent"), data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert RentBicycleModel.objects.count() == 1
    rent = RentBicycleModel.objects.first()
    assert rent.renter == user
    assert rent.bicycle == bicycle
    assert mock_start_process_rent.called
    mock_start_process_rent.assert_called_once_with(RentBicycleModel.objects.last().pk, bicycle.pk)


@pytest.mark.django_db
def test_rent_bicycle_view_create_rent_already_rented(api_client, user, bicycle):
    bicycle.is_rented = True
    bicycle.save()

    api_client.login(username="testuser", password="password")

    data = {"bicycle": bicycle.id}

    response = api_client.post(reverse("rent"), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error": "Bicycle is not available"}


@pytest.mark.django_db
def test_rent_bicycle_view_create_rent_user_already_has_rent(
    api_client, user, bicycle, create_rented_bicycle, mock_start_process_rent
):
    api_client.login(username="testuser", password="password")

    data = {"bicycle": bicycle.id}

    response = api_client.post(reverse("rent"), data, format="json")
    response = api_client.post(reverse("rent"), data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error": "You have already rented a bike"}
