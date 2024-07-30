from django.urls import path

from . import views

urlpatterns = [
    path("available/", views.AllBicycleView.as_view(), name="bicycles"),
    path("rent/", views.RentBicycleView.as_view(), name="rent"),
]
