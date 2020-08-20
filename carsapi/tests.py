# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Car, Rating



class CarsTests(APITestCase):
    def setUp(self):
        """Populate test database."""
        example_models = ['Accord', 'CR-V', 'Pilot']
        for i in range(3):
            Car.objects.create(make="Honda", model=example_models[i])


    def test_create_car_correct(self):
        cars_before = Car.objects.count()
        url = reverse('cars')
        data = {'make': 'Honda', 'model': 'Odyssey'}
        self.client.post(url, data)
        self.assertEqual(Car.objects.count(), cars_before + 1)

    

    def test_create_car_incorrect(self):
        cars_before = Car.objects.count()
        url = reverse('cars')
        data = {'make': 'XYZ', 'model': 'XYZ'}
        response = self.client.post(url, data)
        self.assertEqual(Car.objects.count(), cars_before)
        self.assertEqual(response.status_code, status. HTTP_500_INTERNAL_SERVER_ERROR)


    def test_rate_car_correct(self):
        car = Car.objects.first()

        url = reverse('rate')
        
        data1 = {'make': car.make, 'model': car.model, 'rating':'4'}
        response = self.client.post(url, data1)

        data2 = {'make': car.make, 'model': car.model, 'rating':'3'}
        response = self.client.post(url, data2)

        car_after = Car.objects.get(pk=car.pk)
        self.assertEqual(car_after.average_rating, 3.5)


    def test_rate_car_incorrect_rating(self):
        car = Car.objects.first()
        url = reverse('rate')
        data1 = {'make': car.make, 'model': car.model, 'rating':'6'}
        response = self.client.post(url, data1)
        self.assertEqual(response.status_code, status. HTTP_500_INTERNAL_SERVER_ERROR)


    def test_rate_car_incorrect_car(self):
        url = reverse('rate')
        data1 = {'make': "XYZ", 'model': "XYZ", 'rating':'3'}
        response = self.client.post(url, data1)
        self.assertEqual(response.status_code, status. HTTP_500_INTERNAL_SERVER_ERROR)


    def test_popular_car_correct(self):
        url = reverse('rate')

        cars = Car.objects.all()
        
        car1 = cars[0]
        car2 = cars[1]
        car3 = cars[2]

        data1 = {'make': car1.make, 'model': car1.model, 'rating':'4'}
        self.client.post(url, data1)

        data2 = {'make': car1.make, 'model': car1.model, 'rating':'3'}
        self.client.post(url, data2)

        data3 = {'make': car2.make, 'model': car2.model, 'rating':'5'}
        self.client.post(url, data3)

        url_popular = reverse('popular')
        response = self.client.get(url_popular)
        
        first = list(response.data)[0]
        second = list(response.data)[1]
        third = list(response.data)[2]

        self.assertEqual(first['model'], car1.model)
        self.assertEqual(second['model'], car2.model)
        self.assertEqual(third['model'], car3.model)
