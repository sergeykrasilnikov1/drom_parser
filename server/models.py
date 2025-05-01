from django.db import models

# Create your models here.

class Car(models.Model):
    model = models.CharField(max_length=255, verbose_name="Model name")
    model_url = models.URLField(verbose_name="Model URL")
    image_url = models.URLField(verbose_name="Image URL")

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

class Complectation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='complectations')
    name = models.CharField(max_length=255, verbose_name="Complectation name")
    volume = models.CharField(max_length=50, verbose_name="Engine volume")
    fuel_type = models.CharField(max_length=50, verbose_name="Fuel type")
    power = models.CharField(max_length=50, verbose_name="Power")
    transmission = models.CharField(max_length=50, verbose_name="Transmission type")
    drive = models.CharField(max_length=50, verbose_name="Drive type")
    price = models.CharField(max_length=50, verbose_name="Price")
    year = models.CharField(max_length=4, verbose_name="Year")

    def __str__(self):
        return f"{self.car.model} - {self.name}"

    class Meta:
        verbose_name = "Complectation"
        verbose_name_plural = "Complectations"
