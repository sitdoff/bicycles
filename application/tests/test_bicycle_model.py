from decimal import Decimal, InvalidOperation

import pytest
from django.conf import settings
from django.db.utils import DataError
from rent.models import BicycleModel


@pytest.mark.django_db
def test_bicycle_model_str():
    bicycle = BicycleModel.objects.create(brand="Trek", cost_per_hour=Decimal("10.00"), is_rented=False)
    assert str(bicycle) == "Trek $10.00 per hour"


@pytest.mark.django_db
def test_create_bicycle():
    bicycle = BicycleModel.objects.create(brand="Giant", cost_per_hour=Decimal("15.00"), is_rented=True)
    assert bicycle.brand == "Giant"
    assert bicycle.cost_per_hour == Decimal("15.00")
    assert bicycle.is_rented is True


@pytest.mark.django_db
def test_bicycle_model_cost_per_hour_max_digits():
    with pytest.raises((DataError, InvalidOperation)):
        BicycleModel.objects.create(brand="Specialized", cost_per_hour=Decimal("1234.56"), is_rented=False)


@pytest.mark.django_db
def test_bicycle_model_cost_per_hour_decimal_places():
    bicycle = BicycleModel.objects.create(brand="Cannondale", cost_per_hour=Decimal("9.999"), is_rented=False)
    assert bicycle.cost_per_hour == Decimal("10.00")


if settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":

    @pytest.mark.django_db
    def test_bicycle_model_brand_max_length():
        with pytest.raises((DataError, InvalidOperation)):
            BicycleModel.objects.create(brand="A" * 51, cost_per_hour=Decimal("10.00"), is_rented=False)
