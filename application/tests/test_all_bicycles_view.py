import pytest
from django.urls import reverse
from rent.models import BicycleModel
from rent.serializers import BicycleSerializer
from rest_framework import status


@pytest.mark.django_db
def test_all_bicycle_view_authenticated(api_client, user, create_bicycles):
    api_client.login(username="testuser", password="password")

    response = api_client.get(reverse("bicycles"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    expected_data = BicycleSerializer(BicycleModel.objects.filter(is_rented=False), many=True).data
    assert response.json() == expected_data


@pytest.mark.django_db
def test_all_bicycle_view_unauthenticated(api_client, create_bicycles):
    response = api_client.get(reverse("bicycles"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_all_bicycle_view_only_available_bikes(api_client, user, create_bicycles):
    api_client.login(username="testuser", password="password")

    response = api_client.get(reverse("bicycles"))

    assert response.status_code == status.HTTP_200_OK

    for bicycle in response.json():
        assert not bicycle["is_rented"]
