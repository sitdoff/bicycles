import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_user(api_client):
    response = api_client.post(
        reverse("user-list"),
        {
            "username": "newuser",
            "password": "newpass123",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["username"] == "newuser"


@pytest.mark.django_db
def test_get_jwt_token(api_client, user):
    response = api_client.post(
        reverse("jwt-create"),
        {
            "username": "testuser",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_jwt_token(api_client, user):
    response = api_client.post(
        reverse("jwt-create"),
        {
            "username": "testuser",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    refresh_token = response.data["refresh"]

    response = api_client.post(
        reverse("jwt-refresh"),
        {
            "refresh": refresh_token,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_protected_endpoint(api_client, user):
    response = api_client.post(
        reverse("jwt-create"),
        {
            "username": "testuser",
            "password": "password",
        },
    )
    access_token = response.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"JWT {access_token}")
    response = api_client.get(reverse("bicycles"))

    assert response.status_code == status.HTTP_200_OK
