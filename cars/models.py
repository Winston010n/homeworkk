from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
