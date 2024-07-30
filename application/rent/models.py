from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class BicycleModel(models.Model):
    """
    Bicycle model.
    """

    brand = models.CharField(max_length=50)
    cost_per_hour = models.DecimalField(max_digits=5, decimal_places=2)
    is_rented = models.BooleanField()

    def __str__(self):
        return f"{self.brand} ${self.cost_per_hour} per hour"


class RentBicycleModel(models.Model):
    """
    Bicycle rental model.
    """

    bicycle = models.ForeignKey(BicycleModel, on_delete=models.CASCADE, related_name="rent")
    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rented_bicycles")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    paid = models.BooleanField(default=False)

    @property
    def cost(self):
        """
        Returns cost of bicycle rent.
        """
        if self.end_time:
            result = self.bicycle.cost_per_hour * Decimal((self.end_time - self.start_time).seconds / 3600)
            return result
        return None
