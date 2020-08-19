from .models import Car, Rating
from .serializers import CarSerializer
from rest_framework import generics
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
import requests
from rest_framework.exceptions import APIException

def check_if_parameter_exists(request, *args):
        for parameter in args:
            if not request.data.get(parameter):
                raise APIException("Check request parameters")
            else:
                return True


class CarsView(APIView):
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    def post(self, request):
        check_if_parameter_exists(request, 'make', 'model')

        make = request.data['make']
        model = request.data['model']

        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json' 
        r = requests.get(url)
        models = [elem['Model_Name'] for elem in r.json()['Results']]

        if model in models:
            car = Car.objects.filter(make=make, model=model).first()
            if car is not None:
                raise APIException("Car of this model and make already exists in database")
            
            new_car = Car(make=make, model=model)
            new_car.save()
            return HttpResponseRedirect(redirect_to=reverse('cars'))
        else:
            raise APIException("Such a car does not exist")


class PopularCarsView(APIView):
    def get(self, request):
        cars = Car.objects.order_by('votes_num').reverse()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class Rate(APIView):
    def post(self, request):
        check_if_parameter_exists(request, "make", "model", "rating")

        if not request.data['rating'].isdigit():
            raise APIException("Incorrect rating value")

        if int(request.data['rating']) > 5 or int(request.data['rating']) < 0:
            raise APIException("Incorrect rating value")

        car = Car.objects.filter(make=request.data['make'], model=request.data['model']).first()
        if car is None:
            raise APIException("No such car in database")

        new_rating = Rating(rating=request.data['rating'], car=car)
        new_rating.save()

        car.average_rating = round(car.car_rating.all().aggregate(Avg('rating'))['rating__avg'], 1)
        car.votes_num = car.car_rating.count()
        car.save()

        car_after = Car.objects.filter(make=request.data['make'], model=request.data['model'])
        serializer = CarSerializer(car_after, many=True)
        return Response(serializer.data)
