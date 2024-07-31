from datetime import datetime
from time import sleep

from celery import shared_task

from .models import BicycleModel, RentBicycleModel


@shared_task
def start_process_rent(rent_id, bicycle_id: int, wait_time: int = 5) -> None:
    """
    The task keeps track of rental time.

    After the bike is returned, the rental object is assigned an end time.
    """
    bicycle: BicycleModel = BicycleModel.objects.get(pk=bicycle_id)
    bicycle.is_rented = True
    bicycle.save()
    while bicycle.is_rented:
        sleep(wait_time)
        bicycle.refresh_from_db()
    rent: RentBicycleModel = RentBicycleModel.objects.get(pk=rent_id)
    rent.end_time = datetime.now()
    rent.save()
