from unittest.mock import patch

from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Car


class CarListAPIViewTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("car-list")
        self.car_data = {
            "name": "Volvo XC60",
            "description": "Кроссовер",
            "price": "25000.00",
            "year": 2022,
        }

    def tearDown(self):
        cache.clear()

    def test_get_reads_database_and_caches_result(self):
        Car.objects.create(**self.car_data)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Volvo XC60")
        self.assertIsNotNone(cache.get("cache_key"))

    def test_get_returns_cached_result_without_querying_database(self):
        Car.objects.create(**self.car_data)
        self.client.get(self.url)

        with patch("cars.views.Car.objects.all", side_effect=AssertionError("Database queried")):
            response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "Volvo XC60")

    def test_post_creates_car_and_invalidates_cache(self):
        cache.set("cache_key", [], timeout=60)

        response = self.client.post(self.url, self.car_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Car.objects.count(), 1)
        self.assertIsNone(cache.get("cache_key"))

        updated_response = self.client.get(self.url)
        self.assertEqual(len(updated_response.data), 1)
        self.assertEqual(updated_response.data[0]["name"], "Volvo XC60")
