import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

import catalog
from catalog.models import User, Director, Country, Film
from catalog.serializers import CountrySerializer


class CountryApiTestCase(TestCase):

    def setUp(self):
        self.admin = User.objects.create(username='admin', is_staff=True)
        self.user1 = User.objects.create(username='user1')

        self.director1 = Director.objects.create(user=self.user1, first_name='David', last_name='Lynch')
        self.country1 = Country.objects.create(name='Poland')
        self.film = Film.objects.create(title='Film 1', description='Description 1', director=self.director1)
        self.film.countries.add(self.country1)
        self.countries = Country.objects.all()

    def test_get(self):
        expected_data = CountrySerializer(self.countries, many=True).data

        url = reverse('country-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_post(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)

        url = reverse('country-list')
        self.assertEqual(1, Country.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Country.objects.all().count())

    def test_post_admin(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.admin)
        url = reverse('country-list')
        self.assertEqual(1, Country.objects.all().count())
        response = self.client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Country.objects.all().count())

    def test_put(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-detail', args=(self.countries[0].id,))

        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_put_admin(self):
        data = {
            'name': 'USA',
        }
        json_data = json.dumps(data)
        url = reverse('country-detail', args=(self.countries[0].id,))
        self.client.force_login(self.admin)
        response = self.client.put(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(url)
        self.assertEqual(data, response.data)

    def test_delete(self):
        self.assertEqual(1, Country.objects.all().count())
        url = reverse('country-detail', args=(self.countries[0].id,))
        response = self.client.delete(url, data=self.countries[0].id, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Country.objects.all().count())

    def test_delete_admin(self):
        self.assertEqual(1, Country.objects.all().count())
        url = reverse('country-detail', args=(self.countries[0].id,))
        self.client.force_login(self.admin)
        response = self.client.delete(url, data=self.countries[0].id, content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Country.objects.all().count())


