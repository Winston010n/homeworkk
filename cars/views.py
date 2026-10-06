from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Car
from .serializers import CarSerializer

CACHE_KEY = "cache_key"


class CarListAPIView(APIView):
    def get(self, request):
        cached_data = cache.get(CACHE_KEY)
        if cached_data is not None:
            return Response(cached_data)

        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        cache.set(CACHE_KEY, serializer.data, timeout=60)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(CACHE_KEY)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
