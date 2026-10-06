from django.urls import path

from .views import CarListAPIView

urlpatterns = [
    path("cars/", CarListAPIView.as_view(), name="car-list"),
]
