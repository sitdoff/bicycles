from django.contrib import admin

from .models import BicycleModel, RentBicycleModel

# Register your models here.


@admin.register(BicycleModel)
class BicycleModelAdmin(admin.ModelAdmin):
    list_display = ("brand", "cost_per_hour", "is_rented")


@admin.register(RentBicycleModel)
class RentBicycleModelAdmin(admin.ModelAdmin):
    list_display = ("bicycle", "renter", "start_time", "end_time")
