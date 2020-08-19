from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
# models.py
    
class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    average_rating = models.FloatField(default=0)
    votes_num = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.make} {self.model}"


class Rating(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5)], default=0)
    car = models.ForeignKey(Car, related_name="car_rating", on_delete=models.CASCADE)

